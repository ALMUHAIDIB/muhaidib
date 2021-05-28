# -*- coding: utf-8 -*-
from odoo import http

# class MmInvoiceStateTracking(http.Controller):
#     @http.route('/mm_invoice_state_tracking/mm_invoice_state_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mm_invoice_state_tracking/mm_invoice_state_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mm_invoice_state_tracking.listing', {
#             'root': '/mm_invoice_state_tracking/mm_invoice_state_tracking',
#             'objects': http.request.env['mm_invoice_state_tracking.mm_invoice_state_tracking'].search([]),
#         })

#     @http.route('/mm_invoice_state_tracking/mm_invoice_state_tracking/objects/<model("mm_invoice_state_tracking.mm_invoice_state_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mm_invoice_state_tracking.object', {
#             'object': obj
#         })