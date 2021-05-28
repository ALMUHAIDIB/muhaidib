from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)

class res_partner_inherit(models.Model):
    _inherit = 'res.partner'

    extension_number = fields.Integer(related='user_id.extension_number', string='Extension Number')
    is_employee = fields.Boolean('Is Employee')

    name = fields.Char(index=True,default="Name",compute="_compute_name",store=True)
    # name = fields.Char(index=True,default="Name",store=True,readonly=True)
    first_name = fields.Char(string="First Name", required=True, )
    middle_name = fields.Char(string="Middle Name", required=True, )
    last_name = fields.Char(string="Last Name", required=True, )
    phone = fields.Char(required=True,)
    mobile = fields.Char(required=True,)
    mobile_2 = fields.Char()
    customer_code = fields.Char(string="Customer Code", required=False,readonly=True, default='New' )
    landmark = fields.Char(string="Land Mark" )
    about_us_id = fields.Many2one(comodel_name="about.us", string="How did you hear about us?", required=True, )
    vendor_id = fields.Many2one(comodel_name="res.vendor", string="Vendor", required=False, )
    rel_ids = fields.Many2many(comodel_name="rel.product.partner",  string="Rel Product Partner" )
    rel_waranty_ids = fields.Many2many(comodel_name="rel.product.partner",relation="product_partner", column1="pro", column2="par",   string="Rel Product Partner",domain=lambda self: [('id', 'in', self.rel_ids.ids)] )
    company_type = fields.Selection(string='Company Type',
        selection=[ ('person', 'Individual'),('company', 'Company'),],default="company",)
    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'company'
    date_of_purse = fields.Date(string="Date of Birth", required=False, )
    description_customer_review = fields.Text(string="Description", required=False, )
    attachment_customer_review1 = fields.Binary(string="Attachment", )
    attachment_customer_review2 = fields.Binary(string="Attachment", )
    attachment_customer_review3 = fields.Binary(string="Attachment", )
    attachment_customer_review4 = fields.Binary(string="Attachment", )
    @api.onchange('rel_waranty_ids')
    def onchange_method_rel_waranty_ids(self):
        ids = []
        rel1 = self.env['rel.product.partner'].search([('id', 'in', self.rel_ids.ids)])
        rel2 = self.env['rel.product.partner'].search([('id', 'in', self.rel_waranty_ids.ids)])
        _logger.info("onchange_method_rel_waranty_ids :: ")
        for lien in  rel1:
            ids.append(lien.id)
        _logger.info("pass first loop")
        for line in rel2:
            if line.id not in ids :
                ids.append(line.id)
        _logger.info("pass two loop")

        self.update({
            "rel_ids": [[6, 0, ids]]
        })
    @api.constrains('rel_ids')
    def _check_rel_ids(self):
        for rec in self:
            for line in rec.rel_ids:
                if line.partner_id.id != rec._origin.id:
                    raise ValidationError(_('You cannot Add This Rel'))

    # rel_ids = fields.One2many(comodel_name="rel.product.partner", inverse_name="partner_id", string="Rel Product Partner", required=False, )
    @api.model
    def _default_country(self):
        return self.env['res.country'].search([('code','=','EG')], limit=1)

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=_default_country)


    def _compute_name(self):
        for rec in self:
            _logger.info("here com  name")
            first = ' '
            _logger.info("rec.first_name :: %s",rec.first_name)
            if rec.first_name != False:
                first = str(rec.first_name)
            middle = '  '
            if rec.middle_name != False:
                middle = str(rec.middle_name)
            last = ' '
            if rec.last_name != False:
                last = str(rec.last_name)
            rec.name = first + " " + middle + " " + last
            _logger.info("rec.name :: %s",rec.name)

    @api.onchange('first_name', 'middle_name', 'last_name')
    def onchange_method_update_name(self):
        _logger.info("here name")
        # if self.first_name == '':
        #     self.name = str(self.first_name) + " " + str(self.middle_name) + " " + str(self.last_name)
        first = ' '
        if self.first_name != False:
            first = str(self.first_name)
        middle = '  '
        if self.middle_name != False:
            middle = str(self.middle_name)
        last = ' '
        if self.last_name != False:
            last = str(self.last_name)
        self.name = first + " " + middle + " " + last

        # if self.name == '':
        #     self.name = '  '


    @api.model
    def create(self, vals):
        # res = super(res_partner_inherit, self).create(vals)
        sequence_code = 'customer.code.sequence'
        code = str(self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=self.date))
        vals['customer_code'] = code
        return super(res_partner_inherit, self).create(vals)

    _sql_constraints = [
        ('check_name', "CHECK( 1=1 )", 'Contacts require a name'),
    ]

    def action_view_partner_tickets(self):
        self.ensure_one()
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['domain'] = [
            # ('state', 'in', ['posted', 'paid']),
            ('partner_id', 'child_of', self.id),
        ]
        # action['context'] = {'default_type':'out_invoice', 'type':'out_invoice', 'journal_type': 'sale', 'search_default_unpaid': 1}
        return action

    def action_view_partner_log(self):
        self.ensure_one()
        action = self.env.ref('ecomatic_res_partner_custom.log_call_action').read()[0]
        action['domain'] = [
            # ('state', 'in', ['posted', 'paid']),
            ('partner_id', 'child_of', self.id),
        ]
        return action

    def create_ticket(self):
        rel1 = self.env['rel.product.partner'].search([('id', 'in', self.rel_ids.ids)])
        rel2 = self.env['rel.product.partner'].search([('id', 'in', self.rel_waranty_ids.ids)])
        vals = {
            'partner_id': self.id,
            'partner_email': self.email,
            'name': self.name + " Draft Ticket ",
            "rel_ids": [[6, 0, rel1.ids]],
            "rel_waranty_ids": [[6, 0, rel2.ids]],
        }
        ticket = self.env['helpdesk.ticket'].create(vals).sudo()
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['domain'] = [
            ('id', '=', ticket.id),
        ]
        return action
