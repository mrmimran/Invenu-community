# -*- coding: utf-8 -*-

import time
from odoo import models, api, fields,tools
from odoo.exceptions import UserError
from datetime import date, datetime, time
import babel
from datetime import date, datetime, time



class AdvHrLoanAcc(models.Model):
    _inherit = 'hr.advance'

    employee_account_id = fields.Many2one('account.account', string="Advance Account")
    treasury_account_id = fields.Many2one('account.account', string="Treasury Account")
    journal_id = fields.Many2one('account.journal', string="Journal")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('waiting_approval_2', 'Waiting Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', track_visibility='onchange', copy=False, )

    def adv_action_approve(self):
        """This create account move for request.
            """
        advance_approve = self.env['ir.config_parameter'].sudo().get_param('account.advance_approve')
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
        if not contract_obj:
            raise UserError('You must Define a contract for employee')
        if not self.loan_lines:
            raise UserError('You must compute installment before Approved')
        if advance_approve:
            self.write({'state': 'waiting_approval_2'})
        else:
            if not self.employee_account_id or not self.treasury_account_id or not self.journal_id:
                raise UserError("You must enter employee account & Treasury account and journal to approve ")
            if not self.loan_lines:
                raise UserError('You must compute Loan Request before Approved')
            timenow = date.today()
            for loan in self:
                amount = loan.loan_amount
                loan_name = loan.employee_id.name
                reference = loan.name
                journal_id = loan.journal_id.id
                debit_account_id = loan.treasury_account_id.id
                credit_account_id = loan.employee_account_id.id
                partner_name = loan.employee_id.private_street
                analytic_account = loan.analytic_account
                debit_vals = {
                    'name': loan_name,
                    'partner_id': partner_name,
                    'account_id': debit_account_id,
                    'analytic_distribution': (loan.analytic_account and {loan.analytic_account.id: 100})
                                             or (loan.analytic_account.id and {
                        loan.analytic_account.id: 100}),
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                    'adv_id': loan.id,
                }
                credit_vals = {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'partner_id': partner_name,
                    'analytic_distribution': (loan.analytic_account and {loan.analytic_account.id: 100})
                                             or (loan.analytic_account.id and {
                        loan.analytic_account.id: 100}),
                    'journal_id': journal_id,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                    'adv_id': loan.id,
                }
                vals = {
                    'name': 'Advance For' + ' ' + loan_name,
                    'narration': loan_name,
                    'ref': reference,
                    'journal_id': journal_id,
                    'date': timenow,
                    'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                }
                move = self.env['account.move'].create(vals)
                move.action_post()
            self.write({'state': 'approve'})
        return True

    def adv_action_double_approve(self):
        """This create account move for request in case of double approval.
            """
        if not self.employee_account_id or not self.treasury_account_id or not self.journal_id:
            raise UserError("You must enter employee account & Treasury account and journal to approve ")
        if not self.loan_lines:
            raise UserError('You must compute Loan Request before Approved')
        timenow = date.today()
        for loan in self:
            amount = loan.loan_amount
            loan_name = loan.employee_id.name
            reference = loan.name
            journal_id = loan.journal_id.id
            debit_account_id = loan.treasury_account_id.id
            credit_account_id = loan.employee_account_id.id
            partner_name = loan.employee_id.private_street
            analytic_account = loan.analytic_account
            debit_vals = {
                'name': loan_name,
                'partner_id': partner_name,
                'analytic_distribution': (loan.analytic_account and {loan.analytic_account.id: 100})
                                         or (loan.analytic_account.id and {
                    loan.analytic_account.id: 100}),
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
                'adv_id': loan.id,
            }
            credit_vals = {
                'name': loan_name,
                'partner_id': partner_name,
                'analytic_distribution': (loan.analytic_account and {loan.analytic_account.id: 100})
                                         or (loan.analytic_account.id and {
                    loan.analytic_account.id: 100}),
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
                'adv_id': loan.id,
            }
            vals = {
                'name': 'Advance For' + ' ' + loan_name,
                'narration': loan_name,
                'ref': reference,
                'journal_id': journal_id,
                'date': timenow,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }

            move = self.env['account.move'].create(vals)
            move.action_post()
        self.write({'state': 'approve'})

        return True


class AdvHrLoanLineAcc(models.Model):
    _inherit = "hr.advance.line"

    def adv_action_paid_amount(self,month):
        """This create the account move line for payment of each installment.
            """
        timenow = date.today()

        for line in self:
            if line.adv_id.state != 'approve':
                raise UserError("Advance Request must be approved")
            amount = line.amount
            loan_name = line.employee_id.name
            reference = line.adv_id.name
            journal_id = line.adv_id.journal_id.id
            debit_account_id = line.adv_id.employee_account_id.id
            credit_account_id = line.adv_id.treasury_account_id.id
            name = 'Advance/' + ' ' + loan_name + '/' + month
            debit_vals = {
                'name': loan_name,
                'account_id': debit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount > 0.0 and amount or 0.0,
                'credit': amount < 0.0 and -amount or 0.0,
            }
            credit_vals = {
                'name': loan_name,
                'account_id': credit_account_id,
                'journal_id': journal_id,
                'date': timenow,
                'debit': amount < 0.0 and -amount or 0.0,
                'credit': amount > 0.0 and amount or 0.0,
            }

            vals = {
                'name': name,
                'narration': loan_name,
                'ref': reference,
                'journal_id': journal_id,
                'date': timenow,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }

            move = self.env['account.move'].create(vals)
            move.action_post()
        return True


class AdvPayslipAcc(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        for line in self.input_line_ids:
            date_from = self.date_from
            tym = datetime.combine(fields.Date.from_string(date_from), time.min)
            locale = self.env.context.get('lang') or 'en_US'
            month = tools.ustr(babel.dates.format_date(date=tym, format='MMMM-y', locale=locale))
            if line.loan_line_id:
                line.loan_line_id.action_paid_amount(month)
        return super(AdvPayslipAcc, self).action_payslip_done()
