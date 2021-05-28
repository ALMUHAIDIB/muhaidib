# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_invoice_inherit(models.Model):
    _inherit = 'account.invoice'


    bransh_ids = fields.Many2one('res.partner',string="Bransh")


