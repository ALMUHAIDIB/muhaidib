# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_height = fields.Float(string="Height",  required=False, )
    product_width = fields.Float(string="Width",  required=False, )
    product_length = fields.Float(string="Length",  required=False, )
    package_height = fields.Float(string="Height ",  required=False, )
    package_width = fields.Float(string="Width ",  required=False, )
    package_length = fields.Float(string="Length ",  required=False, )
    net_weight = fields.Float(string="Net Weight",  required=False, )
    gross_weight = fields.Float(string="Gross Weight",  required=False, )
    hs_code = fields.Char(string="HS CODE", required=False, )