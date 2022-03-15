# -*- coding: utf-8 -*-
from odoo import http

# class MmDeliveryNoteReport(http.Controller):
#     @http.route('/mm_delivery_note_report/mm_delivery_note_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mm_delivery_note_report/mm_delivery_note_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mm_delivery_note_report.listing', {
#             'root': '/mm_delivery_note_report/mm_delivery_note_report',
#             'objects': http.request.env['mm_delivery_note_report.mm_delivery_note_report'].search([]),
#         })

#     @http.route('/mm_delivery_note_report/mm_delivery_note_report/objects/<model("mm_delivery_note_report.mm_delivery_note_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mm_delivery_note_report.object', {
#             'object': obj
#         })