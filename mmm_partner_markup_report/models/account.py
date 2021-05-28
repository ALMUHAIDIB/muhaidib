from odoo import api, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    is_gsale = fields.Boolean(string="G Sales")
    is_return = fields.Boolean(string="Return")
    is_discount = fields.Boolean(string="Discount")
    is_cogs = fields.Boolean(string="COGS")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gross_sales = fields.Float('Gross Sales')
    return_sales = fields.Float('Return Sales')
    discount_sales = fields.Float('Discount Sales')
    net_sales = fields.Float('Net Sales')
    cogs_sales = fields.Float('Cogs Sales')
    markup = fields.Float('Markup', group_operator="avg")
    margin = fields.Float('Margin', group_operator="avg")

    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     """
    #         Override read_group to calculate the sum of the non-stored fields that depend on the user context
    #     """
    #     res = super(ResPartner, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
    #                                                      orderby=orderby, lazy=lazy)
    #     print(fields)
    #     print(groupby)
    #     if 'markup' in fields and 'cogs_sales' in fields and 'net_sales' in fields:
    #         for line in res:
    #             if line['cogs_sales'] != 0:
    #                 print('cogs_sales >> ', line['cogs_sales'])
    #                 print('net_sales >> ', line['net_sales'])
    #                 print('markup >> ', line['markup'])
    #                 line['markup'] = (line['net_sales'] - line['cogs_sales']) / line['cogs_sales']
    #                 line['markup'] = round(line['markup'], 2)
    #             else:
    #                 line['markup'] = 0
    #     if 'margin' in fields and 'cogs_sales' in fields and 'net_sales' in fields:
    #         for line in res:
    #             if line['net_sales'] != 0:
    #                 line['margin'] = (line['net_sales'] - line['cogs_sales']) / line['net_sales']
    #                 line['margin'] = round(line['margin'], 2)
    #             else:
    #                 line['margin'] = 0
    #     return res
    #

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    markup = fields.Boolean()
