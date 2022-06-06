from odoo import api, models, fields, SUPERUSER_ID, _


class ResCompany(models.Model):
    _inherit = "res.company"

    allowed_days = fields.Integer()


class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    allowed_days = fields.Integer(related='company_id.allowed_days', string="Allowed Days", readonly=False)
