# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrPayslipInput(models.Model):
    """Inherited model for 'hr.payslip.input'"""
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line',
                                   string="Loan Installment",
                                   help="Loan installment")


class HrPayslip(models.Model):
    """Employee payslip"""
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        """Update the computing sheet of a payslip by adding loan details
        to the 'Other Inputs' section."""

        for data in self:
            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return
            loan_line = data.struct_id.rule_ids.filtered(lambda x: x.code == 'LO')
            if loan_line:
                get_amount = self.env['hr.loan'].search([
                    ('employee_id', '=', data.employee_id.id),
                    ('state', '=', 'approve')
                ])
                if get_amount:
                    existing_lines = data.input_line_ids.filtered(lambda x: x.name == 'LO')  # Get existing loan lines
                    existing_loan_ids = existing_lines.mapped('loan_line_id').ids  # Get IDs of existing loan lines
                    for lines in get_amount:
                        for line in lines.loan_lines:
                            if data.date_from <= line.date <= data.date_to and line.id not in existing_loan_ids:
                                if not line.paid:
                                    amount = line.amount
                                    name = loan_line.id
                                    new_name = self.env['hr.payslip.input.type'].search([('name', '=', 'Loan')])
                                    new_line = {
                                        'input_type_id': new_name.id,
                                        'amount': amount,
                                        'name': 'LO',
                                        'loan_line_id': line.id
                                    }
                                    data.input_line_ids = [(0, 0, new_line)]
        return super(HrPayslip, self).compute_sheet()

    def action_payslip_done(self):
        """Mark loan as paid on paying payslip"""
        for line in self.input_line_ids:
            if line.loan_line_id:
                line.loan_line_id.paid = True
                line.loan_line_id.loan_id._compute_loan_amount()
        return super(HrPayslip, self).action_payslip_done()

    def input_data_line(self, name, amount, loan):
        """Add loan details to payslip as other input"""
        check_lines = []
        new_name = self.env['hr.payslip.input.type'].search([('name', '=', 'Loan')])
        line = (0, 0, {
            'input_type_id': new_name.id,
            'amount': amount,
            'name': 'LO',
            'loan_line_id': loan.id
        })
        check_lines.append(line)
        self.input_line_ids = check_lines


class HrPayslipInputType(models.Model):
    """Inherited model for 'hr.payslip.input.type'"""
    _inherit = 'hr.payslip.input.type'

    input_id = fields.Many2one('hr.salary.rule')


class HrSalaryRule(models.Model):
    """New field company_id on salary rule model"""
    _inherit = 'hr.salary.rule'

    company_id = fields.Many2one('res.company', 'Company',
                                 copy=False, readonly=True, help="Comapny",
                                 default=lambda self: self.env.user.company_id)


class HrPayrollStructure(models.Model):
    """New field company_id on 'hr.payroll.structure'"""
    _inherit = 'hr.payroll.structure'

    company_id = fields.Many2one('res.company', 'Company',
                                 copy=False, readonly=True, help="Comapny",
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def _get_default_rule_ids(self):
        return [
            (0, 0, {
                'name': _('Loan'),
                'sequence': 5,
                'code': 'LO',
                'category_id': self.env.ref('aps_ent_loan.loan').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.LO',
                'amount_select': 'code',
                'amount_python_compute': 'result = inputs.LO and - (inputs.LO.amount)'}),
            (0, 0, {
                'name': _('Advance'),
                'sequence': 4,
                'code': 'Adv',
                'category_id': self.env.ref('aps_ent_loan.Adv').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.Adv',
                'amount_select': 'code',
                'amount_python_compute': 'result = inputs.Adv and - (inputs.Adv.amount)'}),
            (0, 0, {
                'name': _('Basic Salary'),
                'sequence': 1,
                'code': 'BASIC',
                'category_id': self.env.ref('hr_payroll.BASIC').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = payslip.paid_amount',
            }),
            (0, 0, {
                'name': _('Gross'),
                'sequence': 100,
                'code': 'GROSS',
                'category_id': self.env.ref('hr_payroll.GROSS').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = categories.BASIC + categories.ALW',
            }),
            (0, 0, {
                'name': _('Deduction'),
                'sequence': 198,
                'code': 'DEDUCTION',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.DEDUCTION',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.DEDUCTION.amount
        result_name = inputs.DEDUCTION.name""",
            }),
            (0, 0, {
                'name': _('Attachment of Salary'),
                'sequence': 174,
                'code': 'ATTACH_SALARY',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.ATTACH_SALARY',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.ATTACH_SALARY.amount
        result_name = inputs.ATTACH_SALARY.name""",
            }),
            (0, 0, {
                'name': _('Assignment of Salary'),
                'sequence': 174,
                'code': 'ASSIG_SALARY',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.ASSIG_SALARY',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.ASSIG_SALARY.amount
        result_name = inputs.ASSIG_SALARY.name""",
            }),
            (0, 0, {
                'name': _('Child Support'),
                'sequence': 174,
                'code': 'CHILD_SUPPORT',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.CHILD_SUPPORT',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.CHILD_SUPPORT.amount
        result_name = inputs.CHILD_SUPPORT.name""",
            }),
            (0, 0, {
                'name': _('Reimbursement'),
                'sequence': 199,
                'code': 'REIMBURSEMENT',
                'category_id': self.env.ref('hr_payroll.ALW').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.REIMBURSEMENT',
                'amount_select': 'code',
                'amount_python_compute': """result = inputs.REIMBURSEMENT.amount
        result_name = inputs.REIMBURSEMENT.name""",
            }),
            (0, 0, {
                'name': _('Net Salary'),
                'sequence': 200,
                'code': 'NET',
                'appears_on_employee_cost_dashboard': True,
                'category_id': self.env.ref('hr_payroll.NET').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = categories.BASIC + categories.ALW + categories.DED',
                'appears_on_employee_cost_dashboard': True,
            })

        ]

    rule_ids = fields.One2many('hr.salary.rule', 'struct_id', string='Salary Rules', default=_get_default_rule_ids)
