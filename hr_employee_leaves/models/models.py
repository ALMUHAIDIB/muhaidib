# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class LcationDate(models.Model):
    _inherit = 'hr.leave.allocation'

    new_data = fields.Date(string="", required=False, )
    annual = fields.Char(string="", required=False, )


class EmployeeLeaves(models.Model):
    _inherit = 'hr.contract'

    leaves = fields.Selection(string="Annual Leaves", selection=[('30days', '30 Days'), ('21days', '21 Days'), ],
                              required=False, )

    # new_data = fields.Date(string="", required=False, )

    @api.multi
    def leave(self):
        contracts = self.env['hr.contract'].search([('state', '=', 'open')])
        for rec in contracts:
            today = datetime.now().date()
            date = 0
            # print(rec.new_data)
            # if (rec.new_data.year != today.year |  (not rec.new_data.year)) :
            #     rec.new_data.year = today.year
            condition = today - rec.date_start
            print(rec.date_start)

            print(condition / 30)
            condition = condition / 30

            if condition.days >= 11:
                if rec['leaves'] == '30days':
                    allocation_day = 30 / 11
                    print(condition.days)
                    emp = self.env['hr.leave.allocation'].search([('employee_id', '=', rec.employee_id.id)
                                                                     , ('holiday_status_id', '=', 5),
                                                                  ('annual', '=', '30')])
                    allocation_day = allocation_day + (condition.days / 11) * 30
                    if not emp:
                        location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                                                                           'holiday_status_id': 5,
                                                                           'type_request_unit': 'day',
                                                                           'new_data': today,
                                                                           'annual': '30',
                                                                           'holiday_type': 'employee',
                                                                           'name': 'Days for limited category with timesheet',
                                                                           'employee_id': rec.employee_id.id})
                        location.action_approve()
                    # elif emp:
                    #     date = (today - emp.new_data) / 30
                    #     if date.days >=11:
                    #
                    #         location = self.env['hr.leave.allocation'].create(
                    #                 {'number_of_days': allocation_day,
                    #                  'holiday_status_id': 5,
                    #                  'type_request_unit': 'day',
                    #                  'new_data': today,
                    #                  'annual': '30',
                    #                  'holiday_type': 'employee',
                    #                  'name': 'Days for limited category with timesheet',
                    #                  'employee_id': rec.employee_id.id})
                    #         location.action_approve()

                if rec['leaves'] == '21days':
                    allocation_day = 21 / 11

                    emp = self.env['hr.leave.allocation'].search(
                        [('employee_id', '=', rec.employee_id.id), ('holiday_status_id', '=', 5),
                         ('annual', '=', '21')])

                    allocation_day = allocation_day + (condition.days / 11) * 21
                    if not emp:
                        print(rec.employee_id.name)
                        location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                                                                           'holiday_status_id': 5,
                                                                           'new_data': today,
                                                                           'annual': '21',
                                                                           'type_request_unit': 'day',
                                                                           'holiday_type': 'employee',
                                                                           'name': 'Days for limited category with timesheet',
                                                                           'employee_id': rec.employee_id.id})
                        location.action_approve()
                    # elif emp:
                    #     date = (today - emp.new_data) / 30
                    #     if date.days >= 11:
                    #         location = self.env['hr.leave.allocation'].create(
                    #             {'number_of_days': allocation_day + emp.number_of_days,
                    #              'holiday_status_id': 5,
                    #              'type_request_unit': 'day',
                    #              'new_data': today,
                    #              'annual': '21',
                    #              'holiday_type': 'employee',
                    #              'name': 'Days for limited category with timesheet',
                    #              'employee_id': rec.employee_id.id})
                    #         location.action_approve()
            else:
                if rec['leaves'] == '30days':

                    allocation_day = 30 / 11
                    allocation_day = allocation_day * condition.days

                    emp = self.env['hr.leave.allocation'].search([('employee_id', '=', rec.employee_id.id)
                                                                     , ('holiday_status_id', '=', 5),
                                                                  ('annual', '=', '30')])

                    if not emp:
                        location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                                                                           'holiday_status_id': 5,
                                                                           'type_request_unit': 'day',
                                                                           'new_data': today,
                                                                           'annual': '30',
                                                                           'holiday_type': 'employee',
                                                                           'name': 'Days for limited category with timesheet',
                                                                           'employee_id': rec.employee_id.id})
                        location.action_approve()
                    # else:
                    #     if allocation_day > emp.number_of_days:
                    #
                    #         location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                    #                                                        'holiday_status_id': 5,
                    #                                                        'type_request_unit': 'day',
                    #                                                        'new_data': today,
                    #                                                        'annual': '30',
                    #                                                        'holiday_type': 'employee',
                    #                                                        'name': 'Days for limited category with timesheet',
                    #                                                        'employee_id': rec.employee_id.id})
                    #         location.action_approve()

                if rec['leaves'] == '21days':

                    allocation_day = 21 / 11
                    allocation_day = allocation_day * condition.days
                    emp = self.env['hr.leave.allocation'].search(
                        [('employee_id', '=', rec.employee_id.id), ('holiday_status_id', '=', 5),
                         ('annual', '=', '21')])
                    if not emp:
                        location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                                                                           'holiday_status_id': 5,
                                                                           'new_data': today,
                                                                           'annual': '21',
                                                                           'type_request_unit': 'day',
                                                                           'holiday_type': 'employee',
                                                                           'name': 'Days for limited category with timesheet',
                                                                           'employee_id': rec.employee_id.id})
                        location.action_approve()
                    # else:
                    #     if allocation_day > emp.number_of_days:
                    #         location = self.env['hr.leave.allocation'].create({'number_of_days': allocation_day,
                    #                                                            'holiday_status_id': 5,
                    #                                                            'type_request_unit': 'day',
                    #                                                            'new_data': today,
                    #                                                            'annual': '21',
                    #                                                            'holiday_type': 'employee',
                    #                                                            'name': 'Days for limited category with timesheet',
                    #                                                            'employee_id': rec.employee_id.id})
                    #         location.action_approve()


class ConvertDurationType(models.Model):
    _inherit = 'hr.leave'

    request_date_from = fields.Datetime('Request Start Date')
    request_date_to = fields.Datetime('Request End Date')
