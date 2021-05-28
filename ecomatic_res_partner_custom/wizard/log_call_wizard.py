# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from openerp import api, fields, models, _
from datetime import datetime,date

import logging
_logger = logging.getLogger(__name__)

class customer_limit_wizard(models.TransientModel):
    _name = "log.call.wizard"

    date = fields.Datetime(string="Date", readonly=True,default=date.today() )
    call_topic = fields.Char(string="Call Topic", required=True, )
    call_description = fields.Text(string="Call Description", required=True, )


    def create_log_call(self):
        partner_id = self.env.context.get('active_id')
        _logger.info("partner_id :: %s",partner_id)
        vals = {
            'partner_id': partner_id,
            'date': self.date,
            'call_topic': self.call_topic,
            'call_description': self.call_description,
        }
        self.env['log.call'].create(vals).sudo()
