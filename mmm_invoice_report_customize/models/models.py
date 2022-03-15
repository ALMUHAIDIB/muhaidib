# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    grn = fields.Char(string="GRN")
