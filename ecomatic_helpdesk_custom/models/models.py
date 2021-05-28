# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class ecomatic_helpdesk_custom(models.Model):
#     _name = 'ecomatic_helpdesk_custom.ecomatic_helpdesk_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100