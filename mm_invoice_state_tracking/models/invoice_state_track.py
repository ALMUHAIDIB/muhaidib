from odoo import models, fields, api,exceptions,_



class InvoiceStateTrackModel(models.Model):
    _name = 'invoice.state.track'

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users',string='Sales Person')
    invoice_id = fields.Many2one('account.invoice',string='Invoice')
    serial = fields.Char(string='Serial')

    status = fields.Selection([
        ('draft', 'draft'), ('open', 'open'),
        ('paid', 'Paid'), ('cancel', 'Cancel')
    ],string='status')









