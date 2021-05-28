# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'


    is_debit = fields.Boolean(string='Is Debit')
    is_credit = fields.Boolean(string='Is Credit')
    is_refund = fields.Boolean(string='Is a Sales Refund')

class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'


    debit_invoice_id = fields.Many2one('account.invoice', string='Debit Note')

    credit_invoice_id = fields.Many2one('account.invoice',string='Credit Note')

    # refund_invoice_id = fields.Many2one(string='Refunds')


    credit = fields.Boolean(related='journal_id.is_credit')
    debit = fields.Boolean(related='journal_id.is_debit')
    is_refund = fields.Boolean(related='journal_id.is_refund')


    debit_invoice_ids = fields.One2many('account.invoice', 'debit_invoice_id')

    credit_invoice_ids = fields.One2many('account.invoice', 'credit_invoice_id')

    refund_type = fields.Selection([('on_delivery', 'On Delivery'), ('after_delivery', 'After Delivery')], string='Refund Type')
    cust_refund_no = fields.Char(string='Customer Refund No.')

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        vals = super(AccountInvoiceInherit, self)._prepare_refund(invoice,date_invoice,date,description,journal_id)
        vals['parent_partner_id'] = self.parent_partner_id.id
        vals['team_id'] = self.team_id.id
        return vals



