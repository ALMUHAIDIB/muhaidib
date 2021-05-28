from odoo import models, fields, api
from datetime import datetime,date

import logging
_logger = logging.getLogger(__name__)

class aboutUsPartner(models.Model):
    _name = 'about.us'

    name = fields.Char(string="Name",default="Name")
