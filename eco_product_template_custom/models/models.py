# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Product Brand')
    style_id = fields.Many2one('product.style', string='Product Style')
    type_id = fields.Many2one('product.type', string='Product Type')
    power_supply_id = fields.Many2one('product.power.supply', string='Power Supply')
    color_id = fields.Many2one('product.color', string='Color')
    product_dimension = fields.Char(string='Product Dimensions')
    cut_off_dimension = fields.Char(string='Cut Off Dimensions')
    terms_conditions = fields.Text(string='Terms and Conditions')
    promotion_percentage = fields.Char(string='Promotion Percentage')
    promotion_price = fields.Char(string='Promotion Price')
    warranty_years = fields.Char(string='Years Of Warranty')
    default_code = fields.Char('Model No.', compute='_compute_default_code',
                               inverse='_set_default_code', store=True)
    material_id = fields.Many2one('product.material', string='Product Material')
    size = fields.Char(string='Size')
    name = fields.Char('Name', compute='compute_name')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search([('default_code', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)

        return recs.name_get()

    @api.depends('brand_id', 'type_id', 'default_code')
    def compute_name(self):
        for rec in self:
            rec.name = str(rec.brand_id.name) + "_" + str(rec.type_id.name) + "[" + str(rec.default_code) + "]"


class ProductBrand(models.Model):
    _name = 'product.brand'
    _rec_name = 'name'
    _description = 'Product Brand'

    name = fields.Char(string='Name')


class ProductStyle(models.Model):
    _name = 'product.style'
    _rec_name = 'name'
    _description = 'Product Style'

    name = fields.Char(string='Name')


class ProductType(models.Model):
    _name = 'product.type'
    _rec_name = 'name'
    _description = 'Product Type'

    name = fields.Char(string='Name')


class PowerSupply(models.Model):
    _name = 'product.power.supply'
    _rec_name = 'name'
    _description = 'Product Power Supply'

    name = fields.Char(string='Name')


class PowerMaterial(models.Model):
    _name = 'product.material'
    _rec_name = 'name'
    _description = 'Product Material'

    name = fields.Char(string='Name')


class ProductColor(models.Model):
    _name = 'product.color'
    _rec_name = 'name'

    name = fields.Char(string='Name')
