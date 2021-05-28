from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from datetime import datetime, date

import logging

_logger = logging.getLogger(__name__)


class relProductPartner(models.Model):
    _name = 'rel.product.partner'

    name = fields.Char(index=True, readonly=True, default="Name", compute="_compute_name")
    purchase_date = fields.Date(string='Purchase Date')
    estimated_start = fields.Date(string='Estimated Start', compute='compute_estimated_start')
    product_id = fields.Many2one(comodel_name="product.template", string="Product", required=True,
                                 domain=[('type', '!=', 'service')])
    product_dimensions = fields.Char(related="product_id.product_dimension", string='Product Dimensions')
    cut_off_dimensions = fields.Char(related="product_id.cut_off_dimension", string='Cut Off Dimensions')
    terms_conditions = fields.Text(related="product_id.terms_conditions", string='Terms and Conditions')
    model_no = fields.Char(related="product_id.default_code", string='Model No.')
    power_supply = fields.Many2one(related="product_id.power_supply_id", string='Power Supply')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    customer_code = fields.Char(related="partner_id.customer_code")
    date_action = fields.Date(string='Your string', default=date.today())
    start_date = fields.Date(string='Start', compute='compute_start_date')
    end_date = fields.Date(string='End', )
    saturation_data = fields.Date(string='saturation data', )
    installation_data = fields.Date(string='Installation data', )
    serial = fields.Char(related="product_id.barcode", string="Serial")
    serial_waranty = fields.Char(string="Serial Waranty", required=False, )
    vendor_id = fields.Many2one(comodel_name="res.vendor", string="Vendor", required=False, )
    note = fields.Text(string="Note", required=False, )
    installation_p_s_ = fields.Char(string=" Installation P.S.", required=False, )
    is_warranty = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="IS warranty", required=True, )

    def _compute_name(self):
        for rec in self:
            rec.name = rec.product_id.name + " - " + rec.partner_id.name
            _logger.info("rec.name :: %s", rec.name)

    @api.model
    @api.depends('purchase_date')
    def compute_estimated_start(self):
        for rec in self:
            if rec.purchase_date:
                date_1 = (datetime.strptime(str(rec.purchase_date), '%Y-%m-%d') + relativedelta(days=+ 60))
                rec.estimated_start = date_1
            else:
                rec.estimated_start = False

    @api.model
    @api.depends('installation_data', 'estimated_start')
    def compute_start_date(self):
        for rec in self:
            print('hi')
            if rec.installation_data:
                if rec.installation_data < rec.estimated_start:
                    rec.start_date = rec.installation_data
                else:
                    rec.start_date = rec.estimated_start
            else:
                rec.start_date = rec.estimated_start
