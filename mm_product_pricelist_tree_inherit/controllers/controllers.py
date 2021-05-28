# -*- coding: utf-8 -*-
from odoo import http

# class MmProductPricelistTreeInherit(http.Controller):
#     @http.route('/mm_product_pricelist_tree_inherit/mm_product_pricelist_tree_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mm_product_pricelist_tree_inherit/mm_product_pricelist_tree_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mm_product_pricelist_tree_inherit.listing', {
#             'root': '/mm_product_pricelist_tree_inherit/mm_product_pricelist_tree_inherit',
#             'objects': http.request.env['mm_product_pricelist_tree_inherit.mm_product_pricelist_tree_inherit'].search([]),
#         })

#     @http.route('/mm_product_pricelist_tree_inherit/mm_product_pricelist_tree_inherit/objects/<model("mm_product_pricelist_tree_inherit.mm_product_pricelist_tree_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mm_product_pricelist_tree_inherit.object', {
#             'object': obj
#         })