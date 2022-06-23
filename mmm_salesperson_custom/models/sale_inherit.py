# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        company_id = self.company_id.id
        salesperson_line = self.env['salesperson.line'].search([('sales_partner_id','=',self.partner_id.id),
                                                                ('company_id','=',company_id)], limit=1)
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'user_id': salesperson_line.user_id.id or self.env.uid
        }
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_sale_note') and self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id

        if self.user_id.id == values.get('user_id'):
            del values['user_id']
        self.update(values)
