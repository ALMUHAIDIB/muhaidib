from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class res_users_inherit(models.Model):
    _inherit = 'res.users'

    # name = fields.Char(string="Name", readonly=False)

    department_ids = fields.Many2many(comodel_name="employee.department", string="Departments", )
