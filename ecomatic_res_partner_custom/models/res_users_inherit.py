# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_users_inherit(models.Model):
    _inherit = 'res.users'


    extension_number=fields.Integer('Extension Number')

