from odoo import models, fields, api,_

class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def return_invoices_with_domain(self):
            tree_view = self.env.ref('account.invoice_tree_with_onboarding')
            form_view = self.env.ref('account.invoice_form')
            kanban_view = self.env.ref('account.invoice_kanban')
            pivot = self.env.ref('account.view_invoice_pivot')
            action =  {
                    'name': _('Invoices'),
                    'view_type': 'form',
                    'view_mode': 'tree,kanban,pivot, form',
                    'res_model': 'account.invoice',
                    'context': {'type':'out_invoice', 'journal_type': 'sale'},
                    'domain': [('type','=','out_invoice')],
                    'res_id': self.id,
                    'view_id': False,
                    'views': [
                        (tree_view.id, 'tree'),
                        (kanban_view.id, 'kanban'),
                        (pivot.id, 'pivot'),
                        (form_view.id, 'form'),
                    ],
                    'type': 'ir.actions.act_window',
                }
            if self.env.user.has_group('sales_team.group_sale_salesman') and not self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                action['domain'] = [('type','=','out_invoice'),('user_id', '=', self.env.user.id)]
            elif self.env.user.has_group('sales_team.group_sale_salesman_all_leads') and not self.env.user.has_group('sales_team.group_sale_manager') :
                action['domain'] = [('type', '=', 'out_invoice'), '|',('user_id', '=', self.env.user.id),('team_id.users', 'in', self.env.user.id)]
            elif self.env.user.has_group('sales_team.group_sale_manager') :
                action['domain'] = [('type', '=', 'out_invoice')]
            return action

    @api.multi
    def return_credit_with_domain(self):
        tree_view = self.env.ref('account.invoice_tree')
        form_view = self.env.ref('account.invoice_form')
        kanban_view = self.env.ref('account.invoice_kanban')
        pivot = self.env.ref('account.view_invoice_pivot')
        action = {
            'name': _('Credit Notes'),
            'view_type': 'form',
            'view_mode': 'tree,kanban,pivot, form',
            'res_model': 'account.invoice',
            'context': {'default_type': 'out_refund', 'type': 'out_refund', 'journal_type': 'sale'},
            'domain': [('type', '=', 'out_refund')],
            'res_id': self.id,
            'view_id': False,
            'views': [
                (tree_view.id, 'tree'),
                (kanban_view.id, 'kanban'),
                (pivot.id, 'pivot'),
                (form_view.id, 'form'),
            ],
            'type': 'ir.actions.act_window',
        }
        if self.env.user.has_group('sales_team.group_sale_salesman') and not self.env.user.has_group(
                'sales_team.group_sale_salesman_all_leads'):
            action['domain'] = [('type', '=', 'out_refund'), ('user_id', '=', self.env.user.id)]
        elif self.env.user.has_group('sales_team.group_sale_salesman_all_leads') and not self.env.user.has_group(
                'sales_team.group_sale_manager'):
            action['domain'] = [('type', '=', 'out_refund'), '|', ('user_id', '=', self.env.user.id),
                                ('team_id.users', 'in', self.env.user.id)]
        elif self.env.user.has_group('sales_team.group_sale_manager'):
            action['domain'] = [('type', '=', 'out_refund')]
        return action
