# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    salesperson_ids = fields.One2many(comodel_name="salesperson.line", inverse_name="sales_partner_id")


class SalespersonLine(models.Model):
    _name = 'salesperson.line'

    sales_partner_id = fields.Many2one(comodel_name="res.partner", string="SalesPerson", required=True)
    user_id = fields.Many2one(comodel_name="res.users", string="MM SalesPerson", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True)
