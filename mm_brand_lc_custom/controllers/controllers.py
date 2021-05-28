# -*- coding: utf-8 -*-
from odoo import http

# class MmBrandLcCustom(http.Controller):
#     @http.route('/mm_brand_lc_custom/mm_brand_lc_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mm_brand_lc_custom/mm_brand_lc_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mm_brand_lc_custom.listing', {
#             'root': '/mm_brand_lc_custom/mm_brand_lc_custom',
#             'objects': http.request.env['mm_brand_lc_custom.mm_brand_lc_custom'].search([]),
#         })

#     @http.route('/mm_brand_lc_custom/mm_brand_lc_custom/objects/<model("mm_brand_lc_custom.mm_brand_lc_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mm_brand_lc_custom.object', {
#             'object': obj
#         })