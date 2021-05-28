# -*- coding: utf-8 -*-
from odoo import http

# class EcomaticHelpdeskCustom(http.Controller):
#     @http.route('/ecomatic_helpdesk_custom/ecomatic_helpdesk_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecomatic_helpdesk_custom/ecomatic_helpdesk_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecomatic_helpdesk_custom.listing', {
#             'root': '/ecomatic_helpdesk_custom/ecomatic_helpdesk_custom',
#             'objects': http.request.env['ecomatic_helpdesk_custom.ecomatic_helpdesk_custom'].search([]),
#         })

#     @http.route('/ecomatic_helpdesk_custom/ecomatic_helpdesk_custom/objects/<model("ecomatic_helpdesk_custom.ecomatic_helpdesk_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecomatic_helpdesk_custom.object', {
#             'object': obj
#         })