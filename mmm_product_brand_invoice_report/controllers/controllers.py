# -*- coding: utf-8 -*-
from odoo import http

# class MmmProductBrandInvoiceReport(http.Controller):
#     @http.route('/mmm_product_brand_invoice_report/mmm_product_brand_invoice_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_product_brand_invoice_report/mmm_product_brand_invoice_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_product_brand_invoice_report.listing', {
#             'root': '/mmm_product_brand_invoice_report/mmm_product_brand_invoice_report',
#             'objects': http.request.env['mmm_product_brand_invoice_report.mmm_product_brand_invoice_report'].search([]),
#         })

#     @http.route('/mmm_product_brand_invoice_report/mmm_product_brand_invoice_report/objects/<model("mmm_product_brand_invoice_report.mmm_product_brand_invoice_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_product_brand_invoice_report.object', {
#             'object': obj
#         })