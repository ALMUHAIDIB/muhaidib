from odoo import models, fields, api, _
from datetime import datetime


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(string='Brand')