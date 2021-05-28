# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_inherit(models.Model):
    _inherit = 'sale.order'


    bransh_ids = fields.Many2one('res.partner',string="Bransh")
    partner_name_ref=fields.Char(store=False, compute='_compute_name')#

    @api.one
    @api.depends('partner_id')
    def _compute_name(self):
        self.partner_name_ref = (self.partner_id.ref if self.partner_id.ref else "") +'-'+self.partner_id.name


    @api.onchange('partner_id')
    def onchange_partner_id_bransh(self):
        if self.partner_id:
             return {'domain': {'bransh_ids': [('id', 'in', self.partner_id.child_ids.ids)]}}
        else:
            return {'domain': {'bransh_ids': [('id', 'in', [])]}}


    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(sale_order_inherit, self)._prepare_invoice()
        invoice_vals.update({
            'bransh_ids':self.bransh_ids.id,
        })
        return invoice_vals



