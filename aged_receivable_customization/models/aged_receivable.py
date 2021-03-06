# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import format_date



class report_account_aged_partner_inherit(models.AbstractModel):
    _inherit = 'account.aged.partner'

    @api.model
    def _get_lines(self, options, line_id=None):
        sign = -1.0 if self.env.context.get('aged_balance') else 1.0
        lines = []
        account_types = [self.env.context.get('account_type')]
        results, total, amls = self.env['report.account.report_agedpartnerbalance'].with_context(
            include_nullified_amount=True)._get_partner_move_lines(account_types, self._context['date_to'], 'posted',
                                                                   30)
        for values in results:
            sales_person = self.env['res.partner'].browse(values['partner_id']).user_id

            if line_id and 'partner_%s' % (values['partner_id'],) != line_id:
                continue
            vals = {
                'id': 'partner_%s' % (values['partner_id'],),
                'name': values['name'],
                'level': 2,
                'columns': [{'name': ''}] * (4 if account_types[-1] == 'receivable' else 3) + [{'name': self.format_value(sign * v)} for v in
                                                 [values['direction'], values['4'],
                                                  values['3'], values['2'],
                                                  values['1'], values['0'], values['total']]],
                'trust': values['trust'],
                'unfoldable': True,
                'unfolded': 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'),
            }
            lines.append(vals)
            if 'partner_%s' % (values['partner_id'],) in options.get('unfolded_lines'):
                for line in amls[values['partner_id']]:
                    aml = line['line']
                    caret_type = 'account.move'
                    if aml.invoice_id:
                        caret_type = 'account.invoice.in' if aml.invoice_id.type in (
                            'in_refund', 'in_invoice') else 'account.invoice.out'
                    elif aml.payment_id:
                        caret_type = 'account.payment'
                    if account_types[-1] == 'receivable':
                        vals = {
                            'id': aml.id,
                            'name': format_date(self.env, aml.date_maturity or aml.date),
                            'class': 'date',
                            'caret_options': caret_type,
                            'level': 4,
                            'parent_id': 'partner_%s' % (values['partner_id'],),
                            'columns': [{'name': v} for v in
                                        [sales_person.name,
                                         aml.journal_id.code, aml.account_id.code, self._format_aml_name(aml)]] + \
                                       [{'name': v} for v in
                                        [line['period'] == 6 - i and self.format_value(sign * line['amount']) or '' for i in
                                         range(7)]],
                            'action_context': aml.get_action_context(),
                        }
                    else:
                        vals = {
                            'id': aml.id,
                            'name': format_date(self.env, aml.date_maturity or aml.date),
                            'class': 'date',
                            'caret_options': caret_type,
                            'level': 4,
                            'parent_id': 'partner_%s' % (values['partner_id'],),
                            'columns': [{'name': v} for v in
                                        [aml.journal_id.code, aml.account_id.code, self._format_aml_name(aml)]] + \
                                       [{'name': v} for v in
                                        [line['period'] == 6 - i and self.format_value(sign * line['amount']) or '' for
                                         i in
                                         range(7)]],
                            'action_context': aml.get_action_context(),
                        }

                    lines.append(vals)
        if total and not line_id:
            total_line = {
                'id': 0,
                'name': _('Total'),
                'class': 'total',
                'level': 2,
                'columns': [{'name': ''}] * (4 if account_types[-1] == 'receivable' else 3) + [{'name': self.format_value(sign * v)} for v in
                                                 [total[6], total[4], total[3], total[2], total[1], total[0],
                                                  total[5]]],
            }
            lines.append(total_line)
        return lines


class AgedAccountRecievableInherit(models.AbstractModel):
    _inherit = 'account.aged.receivable'

    def _get_columns_name(self, options):
        columns = [{}]
        columns += [
            {'name': v, 'class': 'number', 'style': 'white-space:nowrap;'}
            for v in [_("Sales Person"), _("JRNL"), _("Account"), _("Reference"), _("Not due on: %s") % format_date(self.env, options['date']['date']),
                      _("1 - 30"), _("31 - 60"), _("61 - 90"), _("91 - 120"), _("Older"), _("Total")]
        ]
        return columns

