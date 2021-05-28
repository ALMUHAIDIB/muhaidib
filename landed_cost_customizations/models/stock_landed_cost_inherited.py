# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_landed_cost_inherited(models.Model):
    _inherit = 'stock.landed.cost'

    purchase_order_id = fields.Many2one('purchase.order')


    @api.onchange('purchase_order_id')
    def _get_domain_for_pickings(self):
        relation_ids = self.purchase_order_id.picking_ids.ids
        return {'domain': {'picking_ids': [('id', 'in', relation_ids)]}}


    @api.onchange('picking_ids')
    def _get_domain_for_invoices(self):
        invoice_ids=self.env['account.invoice'].search([('purchase_order_id', '=', self.purchase_order_id.id)]).ids
        return {'domain': {'invoice_ids': [('id', 'in', invoice_ids)]}}


    # def _get_invoices_lines(self,vals):
    #
    #     #get lines from selected invoices and create lines in stock.landed.cost.lines
    #     #then set these lines ids to cost_lines field
    #     if vals['invoice_ids']:
    #         print("self .invo ids")
    #         created_ids=[]
    #         for inv in vals['invoice_ids']:
    #             print("inv inv v",vals['invoice_ids'])
    #             for line in inv.invoice_line_ids:
    #                 values = {'product_id': line.product_id.id, 'account_id':line.account_id.id,
    #                           'price_unit':line.price_unit, 'name':line.name,
    #                         'split_method':line.product_id.split_method, 'cost_id':vals['id']}
    #
    #
    #                 created_id=self.env['stock.landed.cost.lines'].create(values)
    #                 created_ids.append(created_id.id)
    #
    #         if len(created_ids)>0:
    #             print("created_ids", created_ids)
    #
    # @api.model
    # def create(self, vals):
    #     print("caret creat")
    #     self._get_invoices_lines(vals)
    #     obj = super(stock_landed_cost_inherited, self).create(vals)
    #     return obj



