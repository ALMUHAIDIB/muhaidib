# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
# from odoo.addons.ehcs_qr_code_base.models.qr_code_base import generate_qr_code

import qrcode
import base64
from io import BytesIO


def generate_qr_code(url):
    qr = qrcode.QRCode(
             version=1,
             error_correction=qrcode.constants.ERROR_CORRECT_M,
             box_size=20,
             border=4,
             )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    temp = BytesIO()
    img.save(temp, format="PNG")
    qr_img = base64.b64encode(temp.getvalue())
    return qr_img


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')
    qr_in_report = fields.Boolean('Show QR in Report')
    qr_value = fields.Char(string='QR Value', compute='get_qr_code_value', store=True)

    @api.multi
    # @api.depends('company_id')
    def get_qr_code_value(self):
        for rec in self:
            qr_value = request.env['ir.config_parameter'].get_param('web.base.url')
            # qr_value = '%s\n %s\n %s\n ' % (rec.company_id.name, rec.company_id.vat, rec.amount_total)
            # qr_value = ''
            if rec.company_id:
                qr_value += 'اسم المورد:' + '%s' % rec.company_id.name
                # qr_value += 'الرقم الضريبي:' + '%s' % rec.company_id.vat
            # if rec.amount_total:
            #     qr_value += 'إجمالى الفاتورة: %s\n' % rec.amount_total
            # if rec.amount_tax:
            #     qr_value += 'قيمه الضريبه: %s\n' % rec.amount_tax
            # if rec.date_invoice:
            #     qr_value += 'تاريخ الفاتورة: %s\n' % rec.date_invoice
            # if rec.number:
            #     qr_value += 'رقم الفاتورة: %s\n' % rec.number
            return qr_value

    @api.one
    def _generate_qr_code(self):
        self.qr_image = generate_qr_code(self.get_qr_code_value())

    @api.depends('origin')
    def compute_sale_picking_ids(self):
        for record in self:
            if record.origin:
                sale_order = record.env['sale.order'].search([('name', '=', record.origin)])
                record.sale_picking_ids = [(6, 0, sale_order.picking_ids.ids)]

    @api.depends('invoice_line_ids', 'amount_untaxed')
    def get_discount_amount(self):
        for rec in self:
            rec.discount_amount = sum([x.quantity*x.price_unit*x.discount/100 for x in rec.invoice_line_ids])
            rec.total_discount = rec.discount_amount + rec.amount_untaxed

    partner_limit_days = fields.Integer(related='parent_partner_id.credit_period', string='Customer Limit Days',
                                        readonly=True)

    sale_picking_ids = fields.Many2many(comodel_name='stock.picking', readonly=True, compute='compute_sale_picking_ids')

    parent_partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')

    total_discount = fields.Monetary(string='Total Amount', compute="get_discount_amount")
    discount_amount = fields.Monetary(string='Discount Amount', compute="get_discount_amount")

    @api.onchange('parent_partner_id')
    def parent_partner_id_onchange(self):
        if self.parent_partner_id:
            return {'domain': {'partner_id': [('id', 'in', self.parent_partner_id.child_ids.ids)]}}
        else:
            return {'domain': {'partner_id': [('id', 'in', [])]}}

    @api.multi
    def amount_to_text(self, amount):
        return self.currency_id.amount_to_text(amount)

    @api.multi
    def sale_picking_to_text(self, sale_picking):
        sale_picking_text = ''
        for picking in sale_picking:
            sale_picking_text = sale_picking_text+picking.name + '  '
        return sale_picking_text


class AccountInvoiceLineInherit(models.Model):
    _inherit = 'account.invoice.line'

    @api.depends('product_id')
    def compute_partner_sku(self):
        for record in self:
            if record.invoice_id.parent_partner_id and record.product_id:
                partner_id = record.invoice_id.parent_partner_id
                for product in partner_id.customer_product_sku:
                    if record.product_id.id == product.name.id:
                        record.partner_sku = product.product_sku
                record.barcode = record.product_id.barcode

    partner_sku = fields.Char(string='Customer SKU', readonly=True, compute='compute_partner_sku')
    barcode = fields.Char(string='Barcode', compute='compute_partner_sku')




