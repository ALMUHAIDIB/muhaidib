# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(required=True, string='Name')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Product Brand", required=False, )


class InvoicesStatistics(models.Model):
    _inherit = 'account.invoice.report'

    product_brand = fields.Char(string='Product Brand', readonly=True)
    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand List", readonly=True)
    # product_brand = fields.Char(string='Brand List', readonly=True)

    def _select(self):
        res = super(InvoicesStatistics, self)._select()
        print(res)
        return res + ", sub.product_brand, sub.product_brand_id"

    def _sub_select(self):
        res = super(InvoicesStatistics, self)._sub_select()
        print(res)
        return res + ", pt.brand as product_brand, pt.product_brand_id as product_brand_id"

    def _group_by(self):
        res = super(InvoicesStatistics, self)._group_by()
        print(res)
        return res + ", pt.brand, pt.product_brand_id"
