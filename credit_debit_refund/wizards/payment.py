from odoo import models, fields, api


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'


    salary_rec_number = fields.Char(string='Receipt Ref')