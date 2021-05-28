# -*- coding: utf-8 -*-
from odoo import http

# class MmmUniqueInternalRef(http.Controller):
#     @http.route('/mmm_unique_internal_ref/mmm_unique_internal_ref/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_unique_internal_ref/mmm_unique_internal_ref/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_unique_internal_ref.listing', {
#             'root': '/mmm_unique_internal_ref/mmm_unique_internal_ref',
#             'objects': http.request.env['mmm_unique_internal_ref.mmm_unique_internal_ref'].search([]),
#         })

#     @http.route('/mmm_unique_internal_ref/mmm_unique_internal_ref/objects/<model("mmm_unique_internal_ref.mmm_unique_internal_ref"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_unique_internal_ref.object', {
#             'object': obj
#         })