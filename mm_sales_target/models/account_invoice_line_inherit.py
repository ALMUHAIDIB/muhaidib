from odoo import models, fields, api

class AccountInvoiceLineInherit(models.Model):
    _inherit = 'account.invoice.line'

    salesman_id = fields.Many2one(related='invoice_id.user_id', store=True, string='Salesperson')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], related='invoice_id.state',string='Status', store=True,default='draft', copy=False)

