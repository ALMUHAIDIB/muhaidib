# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, models, fields, _
from datetime import timedelta, date


class sale_order(models.Model):
    _inherit = 'sale.order'

    exceeded_amount = fields.Float('Exceeded Amount')
    is_over_due = fields.Boolean(string="Over Due", copy=False)
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('over_due', 'Over Due'),
        ('credit_limit', 'Credit limit'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')

    # @api.multi
    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     super(sale_order,self).onchange_partner_id()
    #     if self.partner_id:
    #         if self.partner_id.credit_limit_on_hold:
    #             msg = "Customer '" + self.partner_id.name + "' is on credit limit hold."
    #             return {'warning':
    #                         {'title': 'Credit Limit On Hold', 'message': msg
    #                          }
    #                     }
    @api.multi
    def check_balance(self):
        for rec in self:
            new_date = rec.date_order.date() - timedelta(days=rec.company_id.allowed_days)
            print("new_date >> ", new_date)
            amount_residual = self.env['account.move.line'].search([
                ('partner_id', '=', rec.parent_partner_id.id),
                ('account_id', '=', rec.partner_id.property_account_receivable_id.id),
                ('date_maturity', '<=', new_date)]).mapped('amount_residual')
            print("amount_residual >> ", amount_residual)
            total_residual = sum(amount_residual)
            print("total_residual >> ", total_residual)
            if total_residual > 0:
                imd = self.env['ir.model.data']
                text = _('This Customer Has Outstanding Amount For More Than %s Days, With Amount Of %s') % (str(rec.company_id.allowed_days), str(total_residual))
                vals_wiz = {
                    'sale_id': rec.id,
                    'text': text,
                }
                wiz_id = self.env['over.due.wizard'].create(vals_wiz)
                action = imd.xmlid_to_object('dev_customer_credit_limit.action_over_due_wizard')
                form_view_id = imd.xmlid_to_res_id('dev_customer_credit_limit.view_over_due_wizard_form')
                return {
                    'name': action.name,
                    'type': action.type,
                    'views': [(form_view_id, 'form')],
                    'view_id': form_view_id,
                    'target': action.target,
                    'context': action.context,
                    'res_model': action.res_model,
                    'res_id': wiz_id.id,
                }
            else:
                rec.is_over_due = True

    @api.multi
    @api.onchange('parent_partner_id')
    def parent_partner_id_onchange(self):
        domain = super(sale_order, self).parent_partner_id_onchange()
        if self.parent_partner_id:
            if self.parent_partner_id.credit_limit_on_hold:
                msg = "Customer '" + self.parent_partner_id.name + "' is on credit limit hold."
                return {'domain': domain['domain'] if domain != None else [],
                        'warning':
                            {'title': 'Credit Limit On Hold', 'message': msg
                             }
                        }
            else:
                return domain

    @api.multi
    def action_sale_ok(self):
        if self.parent_partner_id.check_credit:
            domain = [
                ('order_id.parent_partner_id', '=', self.parent_partner_id.id),
                ('order_id.state', 'in', ['sale', 'credit_limit'])]
            order_lines = self.env['sale.order.line'].search(domain)

            order = []
            to_invoice_amount = 0.0
            for line in order_lines:
                not_invoiced = line.product_uom_qty - line.qty_invoiced
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(
                    price, line.order_id.currency_id,
                    not_invoiced,
                    product=line.product_id, partner=line.order_id.parent_partner_id)
                if line.order_id.id not in order:
                    if line.order_id.invoice_ids:
                        for inv in line.order_id.invoice_ids:
                            if inv.state == 'draft':
                                order.append(line.order_id.id)
                                break
                    else:
                        order.append(line.order_id.id)

                to_invoice_amount += taxes['total_included']

            domain = [
                ('invoice_id.parent_partner_id', '=', self.parent_partner_id.id),
                ('invoice_id.state', '=', 'draft'),
                ('sale_line_ids', '!=', False)]
            draft_invoice_lines = self.env['account.invoice.line'].search(domain)
            for line in draft_invoice_lines:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price, line.invoice_id.currency_id,
                    line.quantity,
                    product=line.product_id, partner=line.invoice_id.parent_partner_id)
                to_invoice_amount += taxes['total_included']

            # We sum from all the invoices lines that are in draft and not linked
            # to a sale order
            domain = [
                ('invoice_id.parent_partner_id', '=', self.parent_partner_id.id),
                ('invoice_id.state', '=', 'draft'),
                ('sale_line_ids', '=', False)]
            draft_invoice_lines = self.env['account.invoice.line'].search(domain)
            draft_invoice_lines_amount = 0.0
            invoice=[]
            for line in draft_invoice_lines:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price, line.invoice_id.currency_id,
                    line.quantity,
                    product=line.product_id, partner=line.invoice_id.parent_partner_id)
                draft_invoice_lines_amount += taxes['total_included']
                if line.invoice_id.id not in invoice:
                    invoice.append(line.invoice_id.id)

            available_credit = self.parent_partner_id.credit_limit - self.parent_partner_id.credit - to_invoice_amount - draft_invoice_lines_amount

            if self.amount_total > available_credit:
                imd = self.env['ir.model.data']
                exceeded_amount = (to_invoice_amount + draft_invoice_lines_amount + self.parent_partner_id.credit + self.amount_total) - self.parent_partner_id.credit_limit
                vals_wiz={
                    'partner_id':self.parent_partner_id.id,
                    'sale_orders':str(len(order))+ ' Sale Order Worth : '+ str(to_invoice_amount),
                    'invoices':str(len(invoice))+' Draft Invoice worth : '+ str(draft_invoice_lines_amount),
                    'current_sale':self.amount_total or 0.0,
                    'exceeded_amount':exceeded_amount,
                    'credit':self.parent_partner_id.credit,
                    'credit_limit_on_hold':self.parent_partner_id.credit_limit_on_hold,
                }
                wiz_id = self.env['customer.limit.wizard'].create(vals_wiz)
                action = imd.xmlid_to_object('dev_customer_credit_limit.action_customer_limit_wizard')
                form_view_id = imd.xmlid_to_res_id('dev_customer_credit_limit.view_customer_limit_wizard_form')
                return {
                    'name': action.name,
                    'help': action.help,
                    'type': action.type,
                    'views': [(form_view_id, 'form')],
                    'view_id': form_view_id,
                    'target': action.target,
                    'context': action.context,
                    'res_model': action.res_model,
                    'res_id':wiz_id.id,
                }
            else:
                self.action_confirm()
        else:
            self.action_confirm()
        return True

    @api.multi
    def _make_url(self, model='sale.order'):
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url', default='http://localhost:8069')
        if base_url:
            base_url += '/web/login?db=%s&login=%s&key=%s#id=%s&model=%s' % (self._cr.dbname, '', '', self.id, model)
        return base_url

    @api.multi
    def send_mail_approve_credit_limit(self):
        manager_group_id = self.env['ir.model.data'].get_object_reference('sales_team', 'group_sale_manager')[1]
        browse_group = self.env['res.groups'].browse(manager_group_id)

        url = self._make_url('sale.order')
        subject = self.name + '-' + 'Require to Credit Limit Approval'
        for user in browse_group.users:
            partner = user.partner_id
            body = '''
                        <b>Dear ''' " %s</b>," % (partner.name) + '''
                        <p> A Sale Order ''' "<b><i>%s</i></b>" % self.name + '''  for customer ''' "<b><i>%s</i></b>" % self.partner_id.name + ''' require your Credit Limit Approval.</p> 
                        <p>You can access sale order from  below url <br/>
                        ''' "%s" % url + ''' </p> 
                        
                        <p><b>Regards,</b> <br/>
                        ''' "<b><i>%s</i></b>" % self.user_id.name + ''' </p> 
                        '''

            mail_values = {
                'email_from': self.user_id.email,
                'email_to': partner.email,
                'subject': subject,
                'body_html': body,
                'state': 'outgoing',
                'type': 'email',
            }
            mail_id = self.env['mail.mail'].create(mail_values)
            mail_id.send(True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
