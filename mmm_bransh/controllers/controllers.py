# -*- coding: utf-8 -*-
from odoo import http

# class MmmBransh(http.Controller):
#     @http.route('/mmm_bransh/mmm_bransh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_bransh/mmm_bransh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_bransh.listing', {
#             'root': '/mmm_bransh/mmm_bransh',
#             'objects': http.request.env['mmm_bransh.mmm_bransh'].search([]),
#         })

#     @http.route('/mmm_bransh/mmm_bransh/objects/<model("mmm_bransh.mmm_bransh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_bransh.object', {
#             'object': obj
#         })