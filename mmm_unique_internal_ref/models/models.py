# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.one
    @api.constrains('default_code')
    def _check_default_code(self):
        if self.default_code and self.search([('default_code', '=', self.default_code),
                                              ('id', '!=', self.id)]):
            raise ValidationError('An Internal reference can only be assigned to one product !')


    # @api.constrains('default_code')
    # def _check_default_code(self):
    #     print('hi')
    #     templates = self.env['product.template'].search([('default_code', '=', self.default_code)]).ids
    #     print(templates)
    #     if len(templates) > 1:
    #         print('validation error')

