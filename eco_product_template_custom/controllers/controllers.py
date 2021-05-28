# -*- coding: utf-8 -*-
# from odoo import http


# class EcoProductTemplateCustom(http.Controller):
#     @http.route('/eco_product_template_custom/eco_product_template_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eco_product_template_custom/eco_product_template_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eco_product_template_custom.listing', {
#             'root': '/eco_product_template_custom/eco_product_template_custom',
#             'objects': http.request.env['eco_product_template_custom.eco_product_template_custom'].search([]),
#         })

#     @http.route('/eco_product_template_custom/eco_product_template_custom/objects/<model("eco_product_template_custom.eco_product_template_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eco_product_template_custom.object', {
#             'object': obj
#         })
