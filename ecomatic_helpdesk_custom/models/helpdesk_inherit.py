from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date

import logging

_logger = logging.getLogger(__name__)


class helpdesk_ticket_inherit(models.Model):
    _inherit = 'helpdesk.ticket'

    stage_id = fields.Many2one('helpdesk.stage', string='Stage', ondelete='restrict', tracking=True,
                               group_expand='_read_group_stage_ids', copy=False,
                               index=True, domain="[('team_ids', '=', False)]")

    name = fields.Char(string='Subject', index=True, readonly=True)

    is_close = fields.Boolean(related="stage_id.is_close")
    is_in_progress = fields.Boolean(related="stage_id.is_in_progress")
    is_solved_stage = fields.Boolean(related="stage_id.is_solved_stage")
    is_draft_stage = fields.Boolean(related="stage_id.is_draft_stage")

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        if self.stage_id.is_in_progress != True and self.stage_id.is_draft_stage != True:
            if self.employee_ticket_id.id == False:
                raise ValidationError(_('You Must Add Employee'))
            if self.description_visite1 == False:
                raise ValidationError(_('You Must Visit Description'))

        if self.stage_id.is_in_progress != True and self.stage_id.is_draft_stage != True and self.stage_id.is_solved_stage != True:
            if self.description_customer_review_more == False:
                raise ValidationError(_('You Must Customer Review Description'))

    # rel_ids = fields.Many2many(related="partner_id.rel_ids", string="Rel Product Partner", )
    # rel_waranty_ids = fields.Many2many(related="partner_id.rel_waranty_ids", string="Rel Product Partner", )
    phone = fields.Char(related="partner_id.phone", required=False, )
    mobile = fields.Char(related="partner_id.mobile", required=False, )
    mobile_2 = fields.Char(related="partner_id.mobile_2", required=False, )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name
            self.partner_email = self.partner_id.email
            rel1 = self.env['rel.product.partner'].search([('id', 'in', self.partner_id.rel_ids.ids)])
            rel2 = self.env['rel.product.partner'].search([('id', 'in', self.partner_id.rel_waranty_ids.ids)])

            self.update({
                "rel_ids": [[6, 0, rel1.ids]],
                "rel_waranty_ids": [[6, 0, rel2.ids]],
            })

    rel_ids = fields.Many2many(comodel_name="rel.product.partner", relation="product_partner_helpdesk1", column1="pro",
                               column2="par", string="Rel Product Partner")

    @api.onchange('rel_ids')
    def onchange_method_rel_ids(self):
        self.partner_id.rel_ids = [[6, 0, self.rel_ids.ids]]

    rel_waranty_ids = fields.Many2many(comodel_name="rel.product.partner", relation="product_partner_helpdesk2",
                                       column1="pro", column2="par", string="Rel Product Partner",
                                       domain=lambda self: [('id', 'in', self.rel_ids.ids)])
    ticket_device_ids = fields.Many2many(required=True, comodel_name="rel.product.partner",
                                         relation="product_partner_helpdesk3", column1="pro", column2="par",
                                         string="Rel Product Partner",
                                         domain=lambda self: [('id', 'in', self.rel_ids.ids)])

    @api.onchange('ticket_device_ids')
    def onchange_method_ticket_device_ids(self):
        ids = []
        rel1 = self.env['rel.product.partner'].search([('id', 'in', self.rel_ids.ids)])
        rel2 = self.env['rel.product.partner'].search([('id', 'in', self.ticket_device_ids.ids)])
        # if len(rel2) > 1 :
        #     raise ValidationError(_('You cannot Add More Than One'))

        _logger.info("onchange_method_ticket_device_ids :: ")
        for lien in rel1:
            ids.append(lien.id)
        _logger.info("pass first loop")
        for line in rel2:
            if line.id not in ids:
                ids.append(line.id)
        _logger.info("pass two loop")

        self.update({
            "rel_ids": [[6, 0, ids]]
        })

    @api.onchange('rel_waranty_ids')
    def onchange_method_rel_waranty_ids(self):
        ids = []
        rel1 = self.env['rel.product.partner'].search([('id', 'in', self.partner_id.rel_ids.ids)])
        rel2 = self.env['rel.product.partner'].search([('id', 'in', self.partner_id.rel_waranty_ids.ids)])
        _logger.info("onchange_method_rel_waranty_ids :: ")
        for lien in rel1:
            ids.append(lien.id)
        _logger.info("pass first loop")
        for line in rel2:
            if line.id not in ids:
                ids.append(line.id)
        _logger.info("pass two loop")

        self.update({
            "rel_ids": [[6, 0, ids]]
        })
        # self.partner_id.rel_waranty_ids = [[6, 0, self.rel_waranty_ids.ids]]

    street = fields.Char(related="partner_id.street", required=False, )
    street2 = fields.Char(related="partner_id.street2", required=False, )
    city = fields.Char(related="partner_id.city", required=False, )
    landmark = fields.Char(related="partner_id.landmark", required=False, )
    state_id = fields.Many2one(related="partner_id.state_id", required=False, )
    zip = fields.Char(related="partner_id.zip", required=False, )
    country_id = fields.Many2one(related="partner_id.country_id", required=False, )

    Visit_scheduled_date = fields.Date(string="Visit scheduled date", required=False, )

    address = fields.Text(string="Address", required=False, compute="_compute_address")
    is_custom_address = fields.Boolean(string="Custom Address", )
    custom_address = fields.Text(string="Address", required=False, )
    description_visite1 = fields.Text(string="Description", required=False, )
    attachment1 = fields.Binary(string="Attachment", )
    description_visite2 = fields.Text(string="Description", required=False, )
    attachment2 = fields.Binary(string="Attachment", )
    description_visite3 = fields.Text(string="Description", required=False, )
    attachment3 = fields.Binary(string="Attachment", )
    description_visite4 = fields.Text(string="Description", required=False, )
    attachment4 = fields.Binary(string="Attachment", )
    description_visite5 = fields.Text(string="Description", required=False, )
    attachment5 = fields.Binary(string="Attachment", )

    description_customer_review_more = fields.Text(string="Description", required=False, )
    description_customer_review = fields.Text(string="Description", required=False, )
    attachment_customer_review1 = fields.Binary(string="Attachment", )
    attachment_customer_review2 = fields.Binary(string="Attachment", )
    attachment_customer_review3 = fields.Binary(string="Attachment", )

    date_delivery1 = fields.Date(string=" Date ", required=False, )
    number_delivery1 = fields.Integer(string="receipt Number", required=False, )
    description_delivery1 = fields.Text(string="Description", required=False, )
    attachment_delivery1 = fields.Binary(string="Attachment", )

    date_delivery2 = fields.Date(string=" Date ", required=False, )
    number_delivery2 = fields.Integer(string="receipt Number", required=False, )
    description_delivery2 = fields.Text(string="Description", required=False, )
    attachment_delivery2 = fields.Binary(string="Attachment", )

    employee_ticket_id = fields.Many2one(comodel_name="employee.ticket", string="Employee", required=False, )

    @api.onchange('employee_ticket_id', 'user_id')
    def _onchange_employee_ticket_id(self):
        _logger.info("enter here")
        if self.user_id.id != False:
            _logger.info("here")
            ids = self.env['employee.department'].search([('id', 'in', self.user_id.department_ids.ids)])
            _logger.info("ids :: %s", ids)
            return {
                'domain': {'employee_ticket_id': [('department_id', 'in', ids.ids)]}
            }

    @api.onchange('partner_id')
    def onchange_method_partner_id(self):
        for rec in self:
            state_id = '  '
            if rec.state_id.name != False:
                state_id = str(rec.state_id.name)
            city = '  '
            if rec.city != False:
                city = str(rec.city)

            street = '  '
            if rec.street != False:
                street = str(rec.street)

            landmark = '  '
            if rec.landmark != False:
                landmark = str(rec.landmark)
            rec.address = state_id + " , " + city + " , " + street + " , " + landmark

    def _compute_address(self):
        for rec in self:
            state_id = '  '
            if rec.state_id.name != False:
                state_id = str(rec.state_id.name)
            city = '  '
            if rec.city != False:
                city = str(rec.city)

            street = '  '
            if rec.street != False:
                street = str(rec.street)

            landmark = '  '
            if rec.landmark != False:
                landmark = str(rec.landmark)
            rec.address = state_id + " , " + city + " , " + street + " , " + landmark

    ticket_code = fields.Char(string="Ticket Code", required=False, readonly=True, default='New')
    date = fields.Datetime(string="Date", readonly=True, default=date.today())

    # is_warranty = fields.Selection(string="IS warranty", selection=[('yes', 'Yes'), ('no', 'No'), ], required=True, )

    @api.constrains('ticket_device_ids')
    def _check_ticket_device_ids(self):
        if self.ticket_device_ids.ids == []:
            raise ValidationError(_('Must Add Ticket Device'))

    @api.model
    def create(self, vals):
        # res = super(helpdesk_ticket_inherit, self).create(vals)
        sequence_code = 'ticket.code.sequence'
        code = str(self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=self.date))
        _logger.info("code ticket :: %s ", code)
        _logger.info("code ticket :: %s ", vals['partner_id'])
        vals['ticket_code'] = code
        partner = self.env['res.partner'].search([('id', '=', vals['partner_id'])], limit=1)
        vals['name'] = str(partner.name) + " / " + code
        _logger.info("ticket_device_ids :: %s", vals["ticket_device_ids"])
        return super(helpdesk_ticket_inherit, self).create(vals)


class helpdesk_stage_inherit(models.Model):
    _inherit = 'helpdesk.stage'

    is_in_progress = fields.Boolean(string="In Progress", )
    is_solved_stage = fields.Boolean(string="In Solved", )
    is_draft_stage = fields.Boolean(string="In Draft", )
