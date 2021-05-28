from odoo import models, fields, api, _
from datetime import datetime

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    sales_person = fields.Many2one('res.users',related='partner_id.user_id',store=True)