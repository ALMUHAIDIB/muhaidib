# -*- coding: utf-8 -*-
from odoo import http

# class EcomaticResPartnerCustom(http.Controller):
#     @http.route('/ecomatic_res_partner_custom/ecomatic_res_partner_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecomatic_res_partner_custom/ecomatic_res_partner_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecomatic_res_partner_custom.listing', {
#             'root': '/ecomatic_res_partner_custom/ecomatic_res_partner_custom',
#             'objects': http.request.env['ecomatic_res_partner_custom.ecomatic_res_partner_custom'].search([]),
#         })

#     @http.route('/ecomatic_res_partner_custom/ecomatic_res_partner_custom/objects/<model("ecomatic_res_partner_custom.ecomatic_res_partner_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecomatic_res_partner_custom.object', {
#             'object': obj
#         })