from odoo import models, fields, api,exceptions,_



class AccountInvoiceModel(models.Model):
    _inherit= 'account.invoice'

    @api.model
    def create(self, vals):
        self.env['invoice.state.track'].create({
                'user_id':vals['user_id'],


            })
        return super(AccountInvoiceModel, self).create(vals)

