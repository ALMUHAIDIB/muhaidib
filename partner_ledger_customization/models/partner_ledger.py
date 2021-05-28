# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.tools import float_is_zero
from odoo.tools.misc import format_date
import io
import datetime
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    # TODO saas-17: remove the try/except to directly import from misc
    import xlsxwriter
from io import BytesIO
import base64
from PIL import Image
import os
import lxml.html


class PartnerLederReportInherit(models.AbstractModel):
    _inherit = 'account.partner.ledger'

    filter_account_matching = False
    filter_branch = True

    @api.model
    def _get_options(self, previous_options=None):
        # Be sure that user has group analytic if a report tries to display analytic
        if self.filter_analytic:
            self.filter_analytic_accounts = [] if self.env.user.id in self.env.ref(
                'analytic.group_analytic_accounting').users.ids else None
            self.filter_analytic_tags = [] if self.env.user.id in self.env.ref(
                'analytic.group_analytic_tags').users.ids else None
            # don't display the analytic filtering options if no option would be shown
            if self.filter_analytic_accounts is None and self.filter_analytic_tags is None:
                self.filter_analytic = None
        if self.filter_partner:
            self.filter_partner_ids = []
            self.filter_partner_categories = []
            self.filter_branch_ids = []
        return self._build_options(previous_options)



    def _get_columns_name(self, options):
        columns = [{}, {'name': _('JRNL')}, {'name': _('Ref')},{'name': _('Branch')}, {'name': _('Sales Person')},
                   {'name': _('Receipt Ref'), 'class': 'number'},
                   {'name': _('Customer Refund No.'), 'class': 'number'},
                   {'name': _('Initial Balance'), 'class': 'number'}, {'name': _('Debit'), 'class': 'number'},
                   {'name': _('Credit'), 'class': 'number'}, {'name': _('Balance'), 'class': 'number'}]

        # if self.user_has_groups('base.group_multi_currency'):
        #     columns.append({'name': _('Amount Currency'), 'class': 'number'})

        return columns


    def _set_context(self, options):
        ctx = super(PartnerLederReportInherit, self)._set_context(options)
        ctx['strict_range'] = True
        if options.get('branch_ids'):
            ctx['branch_ids'] = self.env['res.partner'].browse([int(partner) for partner in options['branch_ids']])
        return ctx

    def _group_by_partner_id(self, options, line_id):  # morad
        partners = {}
        account_types = [a.get('id') for a in options.get('account_type') if a.get('selected', False)]
        if not account_types:
            account_types = [a.get('id') for a in options.get('account_type')]
        date_from = options['date']['date_from']
        results = self._do_query_group_by_account(options, line_id)
        initial_bal_results = self.with_context(
            date_from=False, date_to=fields.Date.from_string(date_from) + datetime.timedelta(days=-1)
        )._do_query_group_by_account(options, line_id)
        context = self.env.context
        base_domain = [('date', '<=', context['date_to']), ('company_id', 'in', context['company_ids']), ('account_id.internal_type', 'in', account_types)]
        base_domain.append(('date', '>=', date_from))
        if context['state'] == 'posted':
            base_domain.append(('move_id.state', '=', 'posted'))
        if options.get('unreconciled'):
            base_domain.append(('full_reconcile_id', '=', False))
        for partner_id, result in results.items():
            domain = list(base_domain)  # copying the base domain
            domain.append(('partner_id', '=', partner_id))
            partner = self.env['res.partner'].browse(partner_id)
            partners[partner] = result
            partners[partner]['initial_bal'] = initial_bal_results.get(partner.id, {'balance': 0, 'debit': 0, 'credit': 0})
            partners[partner]['balance'] += partners[partner]['initial_bal']['balance']
            partners[partner]['total_lines'] = 0
            if not context.get('print_mode'):
                partners[partner]['total_lines'] = self.env['account.move.line'].search_count(domain)
                offset = int(options.get('lines_offset', 0))
                limit = self.MAX_LINES
            #     partners[partner]['lines'] = self.env['account.move.line'].search(domain, order='date,id', limit=limit, offset=offset)
                partners[partner]['lines'] = self.env['account.move.line'].search(domain, order='date,id')
            else:
                partners[partner]['lines'] = self.env['account.move.line'].search(domain, order='date,id')

        # Add partners with an initial balance != 0 but without any AML in the selected period.
        prec = self.env.user.company_id.currency_id.rounding
        missing_partner_ids = set(initial_bal_results.keys()) - set(results.keys())
        for partner_id in missing_partner_ids:
            if not float_is_zero(initial_bal_results[partner_id]['balance'], precision_rounding=prec):
                partner = self.env['res.partner'].browse(partner_id)
                partners[partner] = {'balance': 0, 'debit': 0, 'credit': 0}
                partners[partner]['initial_bal'] = initial_bal_results[partner_id]
                partners[partner]['balance'] += partners[partner]['initial_bal']['balance']
                partners[partner]['lines'] = self.env['account.move.line']
                partners[partner]['total_lines'] = 0

        return partners

    def get_report_informations(self, options):
        '''
        return a dictionary of informations that will be needed by the js widget, manager_id, footnotes, html of report and searchview, ...
        '''
        options = self._get_options(options)
        # apply date and date_comparison filter
        self._apply_date_filter(options)

        searchview_dict = {'options': options, 'context': self.env.context}
        # Check if report needs analytic
        if options.get('analytic_accounts') is not None:
            searchview_dict['analytic_accounts'] = self.env.user.id in self.env.ref(
                'analytic.group_analytic_accounting').users.ids and [(t.id, t.name) for t in
                                                                     self.env['account.analytic.account'].search(
                                                                         [])] or False
            options['selected_analytic_account_names'] = [self.env['account.analytic.account'].browse(int(account)).name
                                                          for account in options['analytic_accounts']]
        if options.get('analytic_tags') is not None:
            searchview_dict['analytic_tags'] = self.env.user.id in self.env.ref(
                'analytic.group_analytic_tags').users.ids and [(t.id, t.name) for t in
                                                               self.env['account.analytic.tag'].search([])] or False
            options['selected_analytic_tag_names'] = [self.env['account.analytic.tag'].browse(int(tag)).name for tag in
                                                      options['analytic_tags']]
        if options.get('partner'):
            options['selected_partner_ids'] = [self.env['res.partner'].browse(int(partner)).name for partner in
                                               options['partner_ids']]
            options['selected_branch_ids'] = [self.env['res.partner'].browse(int(partner)).name for partner in
                                               options['branch_ids']]
            options['selected_partner_categories'] = [self.env['res.partner.category'].browse(int(category)).name for
                                                      category in options['partner_categories']]

        # Check whether there are unposted entries for the selected period or not (if the report allows it)
        if options.get('date') and options.get('all_entries') is not None:
            date_to = options['date'].get('date_to') or options['date'].get('date') or fields.Date.today()
            period_domain = [('state', '=', 'draft'), ('date', '<=', date_to)]
            options['unposted_in_period'] = bool(self.env['account.move'].search_count(period_domain))

        report_manager = self._get_report_manager(options)
        info = {'options': options,
                'context': self.env.context,
                'report_manager_id': report_manager.id,
                'footnotes': [{'id': f.id, 'line': f.line, 'text': f.text} for f in report_manager.footnotes_ids],
                'buttons': self._get_reports_buttons(),
                'main_html': self.get_html(options),
                'searchview_html': self.env['ir.ui.view'].render_template(
                    self._get_templates().get('search_template', 'account_report.search_template'),
                    values=searchview_dict),
                }
        return info

    @api.model
    def _get_lines(self, options, line_id=None):
        offset = int(options.get('lines_offset', 0))
        lines = []
        context = self.env.context
        company_id = context.get('company_id') or self.env.user.company_id
        date_from = options['date']['date_from']           #morad
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()  #morad

        if line_id:
            line_id = int(line_id.split('_')[1]) or None
        elif options.get('partner_ids') and len(options.get('partner_ids')) == 1:
            # If a default partner is set, we only want to load the line referring to it.
            partner_id = options['partner_ids'][0]
            line_id = partner_id
        if line_id:
            if 'partner_' + str(line_id) not in options.get('unfolded_lines', []):
                options.get('unfolded_lines', []).append('partner_' + str(line_id))

        grouped_partners = self._group_by_partner_id(options, line_id)
        if options.get('branch_ids'):
            branch_dict = {}
            partner_obj = self.env['res.partner']
            for branch in options.get('branch_ids'):
                parent = partner_obj.browse(branch).parent_id
                if parent:
                    if parent in grouped_partners:
                        branch_dict[parent] = grouped_partners[parent]
                        data = branch_dict[parent]['lines'].filtered(lambda x: x.invoice_id.partner_id.id == branch or x.payment_id.partner_id.id == branch)
                        lines_before = self.env['account.move.line'].search([('date', '<', date_from),
                                                                             ('partner_id', '=', parent.id),
                                                                             ('account_id.internal_type', '=', 'receivable')])  # morad
                        data_before = lines_before.filtered(lambda x: x.invoice_id.partner_id.id == branch or
                                                                      x.payment_id.partner_id.id == branch)  # morad
                        credit = sum(data.mapped('credit'))
                        debit = sum(data.mapped('debit'))
                        initial_balance = sum(data_before.mapped('debit')) - sum(data_before.mapped('credit'))
                        balance = initial_balance + sum(data.mapped('balance'))
                        branch_dict[parent]['lines'] = data
                        branch_dict[parent]['credit'] = credit
                        branch_dict[parent]['debit'] = debit
                        branch_dict[parent]['balance'] = balance
                        branch_dict[parent]['initial_bal']['balance'] = initial_balance
                        branch_dict[parent]['total_lines'] = len(branch_dict[parent]['lines'])
            if branch_dict:
                grouped_partners = branch_dict
        sorted_partners = sorted(grouped_partners, key=lambda p: p.name or '')
        unfold_all = context.get('print_mode') and not options.get('unfolded_lines')
        total_initial_balance = total_debit = total_credit = total_balance = 0.0
        for partner in sorted_partners:
            debit = grouped_partners[partner]['debit']
            credit = grouped_partners[partner]['credit']
            balance = grouped_partners[partner]['balance']
            initial_balance = grouped_partners[partner]['initial_bal']['balance']
            total_initial_balance += initial_balance
            total_debit += debit
            total_credit += credit
            total_balance += balance
            columns = [self.format_value(initial_balance), self.format_value(debit), self.format_value(credit)]
            # if self.user_has_groups('base.group_multi_currency'):
            #     columns.append('')
            columns.append(self.format_value(balance))
            # don't add header for `load more`
            if offset == 0:
                lines.append({
                    'id': 'partner_' + str(partner.id),
                    'name': partner.name,
                    'columns': [{'name': v} for v in columns],
                    'level': 2,
                    'trust': partner.trust,
                    'unfoldable': True,
                    'unfolded': 'partner_' + str(partner.id) in options.get('unfolded_lines') or unfold_all,
                    'colspan': 7,
                })
            user_company = self.env.user.company_id
            used_currency = user_company.currency_id
            if 'partner_' + str(partner.id) in options.get('unfolded_lines') or unfold_all:
                if offset == 0:
                    progress = initial_balance
                else:
                    progress = float(options.get('lines_progress', initial_balance))
                domain_lines = []
                amls = grouped_partners[partner]['lines']

                remaining_lines = 0
                if not context.get('print_mode'):
                    remaining_lines = grouped_partners[partner]['total_lines'] - offset - len(amls)

                for line in amls:
                    if options.get('cash_basis'):
                        line_debit = line.debit_cash_basis
                        line_credit = line.credit_cash_basis
                    else:
                        line_debit = line.debit
                        line_credit = line.credit
                    date = amls.env.context.get('date') or fields.Date.today()
                    line_currency = line.company_id.currency_id
                    line_debit = line_currency._convert(line_debit, used_currency, user_company, date)
                    line_credit = line_currency._convert(line_credit, used_currency, user_company, date)
                    progress_before = progress
                    progress = progress + line_debit - line_credit
                    caret_type = 'account.move'
                    if line.invoice_id:
                        caret_type = 'account.invoice.in' if line.invoice_id.type in (
                            'in_refund', 'in_invoice') else 'account.invoice.out'
                    elif line.payment_id:
                        caret_type = 'account.payment'
                    domain_columns = [line.journal_id.code, self._format_aml_name(line),
                                      line.invoice_id.partner_id.get_name_ref() or line.payment_id.partner_id.get_name_ref(),
                                      line.invoice_id.user_id.name if line.invoice_id else "",
                                      line.payment_id.salary_rec_number if line.payment_id else "",
                                      line.invoice_id.cust_refund_no if line.invoice_id else "",
                                      self.format_value(progress_before),
                                      line_debit != 0 and self.format_value(line_debit) or '',
                                      line_credit != 0 and self.format_value(line_credit) or '',
                                      self.format_value(progress)]
                    # if self.user_has_groups('base.group_multi_currency'):
                    #     domain_columns.append(self.with_context(no_format=False).format_value(line.amount_currency,
                    #                                                                           currency=line.currency_id) if line.amount_currency != 0 else '')
                    columns = [{'name': v} for v in domain_columns]
                    columns[3].update({'class': 'date'})
                    domain_lines.append({
                        'id': line.id,
                        'parent_id': 'partner_' + str(partner.id),
                        'name': format_date(self.env, line.date),
                        'class': 'date',
                        'columns': columns,
                        'caret_options': caret_type,
                        'level': 4,
                    })

                # load more
                if remaining_lines > 0:
                    domain_lines.append({
                        'id': 'loadmore_%s' % partner.id,
                        'offset': offset + self.MAX_LINES,
                        'progress': progress,
                        'class': 'o_account_reports_load_more text-center',
                        'parent_id': 'partner_%s' % partner.id,
                        'name': _('Load more... (%s remaining)') % remaining_lines,
                        'colspan': 8,
                        'columns': [{}],
                    })
                lines += domain_lines

        if not line_id:
            total_columns = ['', '', '', '', '', '', self.format_value(total_initial_balance),
                             self.format_value(total_debit), self.format_value(total_credit),
                             self.format_value(total_balance)]
            # if self.user_has_groups('base.group_multi_currency'):
            #     total_columns.append('')
            lines.append({
                'id': 'grouped_partners_total',
                'name': _('Total'),
                'level': 0,
                'class': 'o_account_reports_domain_total',
                'columns': [{'name': v} for v in total_columns],
            })
        return lines


    def get_xlsx(self, options, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(self._get_report_name()[:31])
        date_default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2, 'num_format': 'yyyy-mm-dd'})
        date_default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'num_format': 'yyyy-mm-dd'})
        default_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        default_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'bottom': 2})
        super_col_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'align': 'center'})
        level_0_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 6, 'font_color': '#666666'})
        level_1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 13, 'bottom': 1, 'font_color': '#666666'})
        level_2_col1_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_2_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_2_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666'})
        level_3_col1_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666', 'indent': 2})
        level_3_col1_total_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 12, 'font_color': '#666666', 'indent': 1})
        level_3_style = workbook.add_format({'font_name': 'Arial', 'font_size': 12, 'font_color': '#666666'})


        #Set the first column width to 50
        sheet.set_column(0, 0, 50)

        super_columns = self._get_super_columns(options)
        y_offset = bool(super_columns.get('columns')) and 6 or 5


        if self.env.user.company_id.logo:
            value = self.env.user.company_id.logo

            home_dir = os.environ['HOME']
            fh = open(str(home_dir) + "/imageToSave.png", "wb")
            fh.write(base64.b64decode(value))
            fh.close()

            img_name = str(home_dir) + "/imageToSave.png"
            img = Image.open(img_name)
            img = img.resize((140, 115), Image.ANTIALIAS)
            img.info["dpi"] = (96, 96)
            img_name = "{}_resize.{}".format(str(home_dir) + '/test_name_resize', img_name.split('.')[-1])
            img.save(img_name, )

            sheet.insert_image('A1', img_name,
                               {
                                   'x_offset': 1,
                                   'y_offset': 0,
                                   'x_scale': 1.3,
                                   'y_scale': 0.9,
                                   'left': 1,
                                   'url': None,
                                   'tip': None,
                                   'positioning': 1,
                               })

        sheet.write(y_offset, 1, '', title_style)

        # Todo in master: Try to put this logic elsewhere
        x = super_columns.get('x_offset', 0)
        for super_col in super_columns.get('columns', []):
            cell_content = super_col.get('string', '').replace('<br/>', ' ').replace('&nbsp;', ' ')
            x_merge = super_columns.get('merge')
            if x_merge and x_merge > 1:
                sheet.merge_range(0, x, 0, x + (x_merge - 1), cell_content, super_col_style)
                x += x_merge
            else:
                sheet.write(0, x, cell_content, super_col_style)
                x += 1
        for row in self.get_header(options):
            x = 0
            for column in row:
                colspan = column.get('colspan', 1)
                header_label = column.get('name', '').replace('<br/>', ' ').replace('&nbsp;', ' ')
                if colspan == 1:
                    sheet.write(y_offset, x, header_label, title_style)
                else:
                    sheet.merge_range(y_offset, x, y_offset, x + colspan - 1, header_label, title_style)
                x += colspan
            y_offset += 1
        ctx = self._set_context(options)
        ctx.update({'no_format':True, 'print_mode':True})
        lines = self.with_context(ctx)._get_lines(options)

        if options.get('hierarchy'):
            lines = self._create_hierarchy(lines)

        #write all data rows
        for y in range(0, len(lines)):
            level = lines[y].get('level')
            if lines[y].get('caret_options'):
                style = level_3_style
                col1_style = level_3_col1_style
            elif level == 0:
                y_offset += 1
                style = level_0_style
                col1_style = style
            elif level == 1:
                style = level_1_style
                col1_style = style
            elif level == 2:
                style = level_2_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_2_col1_total_style or level_2_col1_style
            elif level == 3:
                style = level_3_style
                col1_style = 'total' in lines[y].get('class', '').split(' ') and level_3_col1_total_style or level_3_col1_style
            else:
                style = default_style
                col1_style = default_col1_style

            if 'date' in lines[y].get('class', ''):
                #write the dates with a specific format to avoid them being casted as floats in the XLSX
                if isinstance(lines[y]['name'], (datetime.date, datetime.datetime)):
                    sheet.write_datetime(y + y_offset, 0, lines[y]['name'], date_default_col1_style)
                else:
                    sheet.write(y + y_offset, 0, lines[y]['name'], date_default_col1_style)
            else:
                #write the first column, with a specific style to manage the indentation
                sheet.write(y + y_offset, 0, lines[y]['name'], col1_style)

            #write all the remaining cells
            for x in range(1, len(lines[y]['columns']) + 1):
                this_cell_style = style
                if 'date' in lines[y]['columns'][x - 1].get('class', ''):
                    #write the dates with a specific format to avoid them being casted as floats in the XLSX
                    this_cell_style = date_default_style
                    if isinstance(lines[y]['columns'][x - 1].get('name', ''), (datetime.date, datetime.datetime)):
                        sheet.write_datetime(y + y_offset, x + lines[y].get('colspan', 1) - 1, lines[y]['columns'][x - 1].get('name', ''), this_cell_style)
                    else:
                        sheet.write(y + y_offset, x + lines[y].get('colspan', 1) - 1, lines[y]['columns'][x - 1].get('name', ''), this_cell_style)
                else:
                    sheet.write(y + y_offset, x + lines[y].get('colspan', 1) - 1, lines[y]['columns'][x - 1].get('name', ''), this_cell_style)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    @api.multi
    def get_html(self, options, line_id=None, additional_context=None):
        '''
        return the html value of report, or html value of unfolded line
        * if line_id is set, the template used will be the line_template
        otherwise it uses the main_template. Reason is for efficiency, when unfolding a line in the report
        we don't want to reload all lines, just get the one we unfolded.
        '''
        # Check the security before updating the context to make sure the options are safe.
        self._check_report_security(options)

        # Prevent inconsistency between options and context.
        self = self.with_context(self._set_context(options))

        templates = self._get_templates()
        report_manager = self._get_report_manager(options)
        report = {'name': self._get_report_name(),
                  'summary': report_manager.summary,
                  'company_name': self.env.user.company_id.name, }
        lines = self._get_lines(options, line_id=line_id)

        if options.get('hierarchy'):
            lines = self._create_hierarchy(lines)

        footnotes_to_render = []
        if self.env.context.get('print_mode', False):
            # we are in print mode, so compute footnote number and include them in lines values, otherwise, let the js compute the number correctly as
            # we don't know all the visible lines.
            footnotes = dict([(str(f.line), f) for f in report_manager.footnotes_ids])
            number = 0
            for line in lines:
                f = footnotes.get(str(line.get('id')))
                if f:
                    number += 1
                    line['footnote'] = str(number)
                    footnotes_to_render.append({'id': f.id, 'number': number, 'text': f.text})

        rcontext = {'report': report,
                    'lines': {'columns_header': self.get_header(options), 'lines': lines},
                    'options': options,
                    'context': self.env.context,
                    'model': self,
                    'user': self.env.user,
                    }
        if additional_context and type(additional_context) == dict:
            rcontext.update(additional_context)
        if self.env.context.get('analytic_account_ids'):
            rcontext['options']['analytic_account_ids'] = [
                {'id': acc.id, 'name': acc.name} for acc in self.env.context['analytic_account_ids']
            ]

        render_template = templates.get('main_template', 'account_reports.main_template')
        if line_id is not None:
            render_template = templates.get('line_template', 'account_reports.line_template')
        html = self.env['ir.ui.view'].render_template(
            render_template,
            values=dict(rcontext),
        )
        if self.env.context.get('print_mode', False):
            for k, v in self._replace_class().items():
                html = html.replace(k, v)
            # append footnote as well
            html = html.replace(b'<div class="js_account_report_footnotes"></div>',
                                self.get_html_footnotes(footnotes_to_render))
        return html


