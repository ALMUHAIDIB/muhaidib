# -*- coding: utf-8 -*-
from odoo import http

# class MmmJournalBranch(http.Controller):
#     @http.route('/mmm_journal_branch/mmm_journal_branch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmm_journal_branch/mmm_journal_branch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmm_journal_branch.listing', {
#             'root': '/mmm_journal_branch/mmm_journal_branch',
#             'objects': http.request.env['mmm_journal_branch.mmm_journal_branch'].search([]),
#         })

#     @http.route('/mmm_journal_branch/mmm_journal_branch/objects/<model("mmm_journal_branch.mmm_journal_branch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmm_journal_branch.object', {
#             'object': obj
#         })