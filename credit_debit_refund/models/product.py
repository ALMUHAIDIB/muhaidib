from odoo import api, models, fields



class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    is_discount = fields.Boolean(string='Is Discount')

    refund_account_id = fields.Many2one(comodel_name='account.account', string='Refund Account')