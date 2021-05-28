from odoo import models, api, fields
from odoo.exceptions import ValidationError



class DebitNote(models.TransientModel):
    _name = 'debit.note'

    def get_currency(self):
        inv_obj = self.env['account.invoice']
        active_id = self.env.context.get('active_id')
        record = inv_obj.browse(active_id)
        return record.currency_id.id


    currency_id = fields.Many2one(comodel_name='res.currency', default = get_currency)
    discount_amount = fields.Monetary(string='Discount Amount', required=True, currency_field='currency_id')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal', domain=[('is_debit', '=', True)])
    discount_product_id = fields.Many2one(comodel_name='product.product', domain=[('is_discount', '=', True)])
    date_debit_note = fields.Date(required=True, string='Debit Note Date', default=fields.Date.today())


    @api.constrains('discount_amount')
    def discount_amount_constrain(self):
        if self.discount_amount == 0.0:
            raise ValidationError("Discount amount Must Not Be Zero")



    def confirm_debit_note(self):
        inv_obj = self.env['account.invoice']
        active_id = self.env.context.get('active_id')
        record = inv_obj.browse(active_id)
        debit_note_lines = self.env['account.invoice.line'].create({
            'name': 'Insurance claim',
            'product_id': self.discount_product_id.id,
            'account_id': self.journal_id.default_debit_account_id.id,
            'quantity': 1,
            'price_unit': self.discount_amount,
        })

        debit_note_lines.write({
            'name': debit_note_lines.with_context(lang=record.partner_id.lang)._get_invoice_line_name_from_product()
        })


        record.debit_invoice_ids = [(0, 0, {
            'partner_id': record.partner_id.id,
            'parent_partner_id': record.parent_partner_id.id,
            'origin': record.number,
            'user_id': record.user_id.id,
            'team_id': record.team_id.id,
            'currency_id': record.currency_id.id,
            'date_invoice': self.date_debit_note,
            'journal_id': self.journal_id.id,
            'invoice_line_ids': [(6, 0, debit_note_lines.ids)],
            'company_id': record.company_id.id,
            'account_id': record.partner_id.property_account_receivable_id.id,
            'type': 'out_invoice',
            'state': 'draft'
        })]



