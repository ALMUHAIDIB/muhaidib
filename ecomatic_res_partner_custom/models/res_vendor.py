from odoo import models, fields, api
from datetime import datetime,date

import logging
_logger = logging.getLogger(__name__)

class ResVendor(models.Model):
    _name = 'res.vendor'

    name = fields.Char(string="Name",default="Name")
    mobile = fields.Char(string="Mobile",)
    address = fields.Char(string="Address")