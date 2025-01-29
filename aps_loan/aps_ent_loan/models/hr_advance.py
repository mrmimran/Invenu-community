# -*- coding: utf-8 -*-

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrAdvance(models.Model):
    """Model for Loan Requests for employees."""
    _name = 'hr.advance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Advance Request"

    @api.model
    def default_get(self, field_list):
        """Retrieve default values for specified fields."""
        result = super(HrAdvance, self).default_get(field_list)
        if result.get('user_id'):
            ts_user_id = result['user_id']
        else:
            ts_user_id = self.env.context.get('user_id', self.env.user.id)
        result['employee_id'] = self.env['hr.employee'].search(
            [('user_id', '=', ts_user_id)], limit=1).id
        return result

    def _compute_loan_amount(self):
        """calculate the total amount paid towards the loan."""
        total_paid = 0.0
        for loan in self:
            for line in loan.loan_lines:
                if line.paid:
                    total_paid += line.amount
            balance_amount = loan.loan_amount - total_paid
            loan.total_amount = loan.loan_amount
            loan.balance_amount = balance_amount
            loan.total_paid_amount = total_paid

    name = fields.Char(string="Advance Name", default="/", readonly=True,
                       help="Name of the Advance")
    date = fields.Date(string="Date", default=fields.Date.today(),
                       readonly=True, help="Date")

    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account")

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  required=True, help="Employee")
    department_id = fields.Many2one('hr.department',
                                    related="employee_id.department_id",
                                    readonly=True,
                                    string="Department", help="Employee")
    installment = fields.Integer(string="No Of Installments", default=1,
                                 help="Number of installments")
    payment_date = fields.Date(string="Payment Start Date", required=True,
                               default=fields.Date.today(),
                               help="Date of the payment")
    loan_lines = fields.One2many('hr.advance.line',
                                 'loan_id', string="Loan Line",
                                 index=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True,
                                 help="Company",
                                 default=lambda self: self.env.user.company_id,
                                 states={'draft': [('readonly', False)]})
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, help="Currency",
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id",
                                   readonly=True, string="Job Position",
                                   help="Job position")
    loan_amount = fields.Float(string="Advance Amount", required=True,
                               help="Advance amount")
    total_amount = fields.Float(string="Total Amount", store=True,
                                readonly=True, compute='_compute_loan_amount',
                                help="Total Advance amount")
    balance_amount = fields.Float(string="Balance Amount", store=True,
                                  compute='_compute_loan_amount',
                                  help="Balance amount")
    total_paid_amount = fields.Float(string="Total Paid Amount", store=True,
                                     compute='_compute_loan_amount',
                                     help="Total paid amount")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', tracking=True, copy=False, )

    @api.model
    def create(self, values):
        """creates a new HR loan record with the provided values."""
        adv_count = self.env['hr.advance'].search_count(
            [('employee_id', '=', values['employee_id']),
             ('state', '=', 'approve'),
             ('balance_amount', '!=', 0)])
        if adv_count:
            raise ValidationError(
                _("The employee has already a pending installment"))
        else:
            values['name'] = self.env['ir.sequence'].get('hr.advance.seq') or ' '
            res = super(HrAdvance, self).create(values)
            return res


    def adv_compute_installment(self):
        """This automatically create the installment the employee need to pay
        to company based on payment start date and the no of installments."""
        for loan in self:
            loan.loan_lines.unlink()
            date_start = datetime.strptime(str(loan.payment_date), '%Y-%m-%d')
            amount = loan.loan_amount / loan.installment
            for i in range(1, loan.installment + 1):
                self.env['hr.advance.line'].create({
                    'date': date_start,
                    'amount': amount,
                    'employee_id': loan.employee_id.id,
                    'loan_id': loan.id})
                date_start = date_start + relativedelta(months=1)
            loan._compute_loan_amount()
        return True

    def adv_action_refuse(self):
        """Action to refuse the loan"""
        return self.write({'state': 'refuse'})

    def adv_action_submit(self):
        """Action to submit the loan"""
        self.write({'state': 'waiting_approval_1'})

    def adv_action_cancel(self):
        """Action to cancel the loan"""
        self.write({'state': 'cancel'})

    def adv_action_approve(self):
        """Approve loan by the manager"""
        for data in self:
            if not data.loan_lines:
                raise ValidationError(_("Please Compute installment"))
            else:
                self.write({'state': 'approve'})

    def unlink(self):
        """Unlink loan lines"""
        for loan in self:
            if loan.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a loan which is not in draft or cancelled state')
        return super(HrAdvance, self).unlink()


class AdvanceLine(models.Model):
    _name = "hr.advance.line"
    _description = "Installment Line"

    date = fields.Date(string="Payment Date", required=True,
                       help="Date of the payment")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help="Employee")
    amount = fields.Float(string="Amount", required=True, help="Amount")
    paid = fields.Boolean(string="Paid", help="Paid")
    loan_id = fields.Many2one('hr.advance', string="Advance Ref.", help="Advance")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.", help="Payslip")


class AdvHrEmployee(models.Model):
    _inherit = "hr.employee"

    def _compute_employee_adv(self):
        """This compute the Advance amount and total Advance count of an employee.
            """
        self.adv_count = self.env['hr.advance'].search_count([('employee_id', '=', self.id)])

    adv_count = fields.Integer(string="Advance", compute='_compute_employee_adv')

