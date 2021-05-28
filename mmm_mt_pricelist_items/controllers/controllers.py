# -*- coding: utf-8 -*-
from odoo import http

# class MmmMtProductList(http.Controller):
#     @http.route('/mmm_mt_product_list/mmm_mt_product_list/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_mt_product_list/mmm_mt_product_list/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_mt_product_list.listing', {
#             'root': '/mmm_mt_product_list/mmm_mt_product_list',
#             'objects': http.request.env['mmm_mt_product_list.mmm_mt_product_list'].search([]),
#         })

#     @http.route('/mmm_mt_product_list/mmm_mt_product_list/objects/<model("mmm_mt_product_list.mmm_mt_product_list"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_mt_product_list.object', {
#             'object': obj
#         })