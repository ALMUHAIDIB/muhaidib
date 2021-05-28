# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PriceListItemInherit(models.Model):
    _inherit = "product.pricelist.item"

    @api.one
    @api.depends('categ_id', 'product_tmpl_id', 'product_id', 'compute_price', 'fixed_price',
                 'pricelist_id', 'percent_price', 'price_discount', 'price_surcharge')
    def _get_pricelist_item_name_price(self):
        if self.categ_id:
            self.name = _("Category: %s") % (self.categ_id.name)
        elif self.product_tmpl_id:
            # self.name = self.product_tmpl_id.name
            self.name = list(self.product_tmpl_id.name_get()[0])[-1]
        elif self.product_id:
            # self.name = self.product_id.display_name.replace('[%s]' % self.product_id.code, '')
            self.name = list(self.product_id.name_get()[0])[-1]
        else:
            self.name = _("All Products")

        if self.compute_price == 'fixed':
            self.price = ("%s %s") % (self.fixed_price, self.pricelist_id.currency_id.name)
        elif self.compute_price == 'percentage':
            self.price = _("%s %% discount") % (self.percent_price)
        else:
            self.price = _("%s %% discount and %s surcharge") % (self.price_discount, self.price_surcharge)

    @api.onchange('product_tmpl_id')
    def product_tmpl_id_onchange(self):
        if self.product_tmpl_id:
            if self.product_tmpl_id in self.pricelist_id.item_ids[:-2].mapped('product_tmpl_id'):
                raise ValidationError(_("Product {0} is already in the PriceList".format(list(self.product_tmpl_id.name_get()[0])[-1])))




