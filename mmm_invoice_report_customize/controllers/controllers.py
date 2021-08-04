# -*- coding: utf-8 -*-
from odoo import http

# class MmmInvoiceReportCustomize(http.Controller):
#     @http.route('/mmm_invoice_report_customize/mmm_invoice_report_customize/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_invoice_report_customize/mmm_invoice_report_customize/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_invoice_report_customize.listing', {
#             'root': '/mmm_invoice_report_customize/mmm_invoice_report_customize',
#             'objects': http.request.env['mmm_invoice_report_customize.mmm_invoice_report_customize'].search([]),
#         })

#     @http.route('/mmm_invoice_report_customize/mmm_invoice_report_customize/objects/<model("mmm_invoice_report_customize.mmm_invoice_report_customize"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_invoice_report_customize.object', {
#             'object': obj
#         })