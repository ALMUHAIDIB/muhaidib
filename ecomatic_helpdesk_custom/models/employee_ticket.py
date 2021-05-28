from odoo import models, fields, api
from datetime import datetime, date

import logging

_logger = logging.getLogger(__name__)


class employeeticket(models.Model):
    _name = 'employee.ticket'

    name = fields.Char(string="Name", required=True)
    department_id = fields.Many2one(comodel_name="employee.department", string="Department", required=True, )


class employeedepartment(models.Model):
    _name = 'employee.department'

    name = fields.Char(string="Name")
