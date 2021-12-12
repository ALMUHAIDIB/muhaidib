# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    l10n_sa_delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today, copy=False)
    l10n_sa_show_delivery_date = fields.Boolean(compute='_compute_show_delivery_date')
    l10n_sa_qr_code_str = fields.Char(string='Zatka QR Code', compute='_compute_qr_code_str')
    l10n_sa_confirmation_datetime = fields.Datetime(string='Confirmation Date', copy=False, readonly=True,
                                                    default=fields.Datetime.now())

    @api.depends('company_id.country_id.code', 'type')
    def _compute_show_delivery_date(self):
        for move in self:
            move.l10n_sa_show_delivery_date = move.company_id.country_id.code == 'SA' and \
                                              move.type in ('out_invoice', 'out_refund')

    @api.depends('amount_total', 'amount_untaxed', 'l10n_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """

        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.l10n_sa_confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            record.l10n_sa_confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(
                    record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.l10n_sa_qr_code_str = qr_code_str

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




