# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import api, fields, models, _


class OverDueWizard(models.TransientModel):
    _name = "over.due.wizard"

    def pass_over_due_balance(self):
        self.sale_id.is_over_due = True

    text = fields.Text(readonly=True, Force_save=True)
    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")