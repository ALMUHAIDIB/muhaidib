# -*- coding: utf-8 -*-
from odoo import http

# class LandedCostCustomizations(http.Controller):
#     @http.route('/landed_cost_customizations/landed_cost_customizations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/landed_cost_customizations/landed_cost_customizations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('landed_cost_customizations.listing', {
#             'root': '/landed_cost_customizations/landed_cost_customizations',
#             'objects': http.request.env['landed_cost_customizations.landed_cost_customizations'].search([]),
#         })

#     @http.route('/landed_cost_customizations/landed_cost_customizations/objects/<model("landed_cost_customizations.landed_cost_customizations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('landed_cost_customizations.object', {
#             'object': obj
#         })