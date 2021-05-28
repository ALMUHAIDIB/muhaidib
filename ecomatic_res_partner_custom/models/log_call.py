from odoo import models, fields, api
from datetime import datetime, date

import logging

_logger = logging.getLogger(__name__)


class aboutUsPartner(models.Model):
    _name = 'log.call'

    # name = fields.Char(string="Name",default="Name")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )
    date = fields.Datetime(string="Date", required=False)
    call_topic = fields.Char(string="Call Topic", required=False, )
    call_description = fields.Text(string="Call Description", required=False, )
