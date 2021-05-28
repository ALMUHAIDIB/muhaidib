# -*- coding: utf-8 -*-
from odoo import http

# class MmmInvoiceTrack(http.Controller):
#     @http.route('/mmm_invoice_track/mmm_invoice_track/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_invoice_track/mmm_invoice_track/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_invoice_track.listing', {
#             'root': '/mmm_invoice_track/mmm_invoice_track',
#             'objects': http.request.env['mmm_invoice_track.mmm_invoice_track'].search([]),
#         })

#     @http.route('/mmm_invoice_track/mmm_invoice_track/objects/<model("mmm_invoice_track.mmm_invoice_track"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_invoice_track.object', {
#             'object': obj
#         })