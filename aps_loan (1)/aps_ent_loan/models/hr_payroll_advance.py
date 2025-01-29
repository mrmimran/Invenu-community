# -*- coding: utf-8 -*-
from odoo import models, fields


class AdvHrPayslipInput(models.Model):
    """Inherited model for 'hr.payslip.input'"""
    _inherit = 'hr.payslip.input'

    adv_line_id = fields.Many2one('hr.advance.line',
                                  string="Advance Installment",
                                  help="Advance installment")


class AdvHrPayslip(models.Model):
    """Employee payslip"""
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        """Update the computing sheet of a payslip by adding Advance details
        to the 'Other Inputs' section."""

        for data in self:
            if (not data.employee_id) or (not data.date_from) or (not data.date_to):
                return
            advance_line = data.struct_id.rule_ids.filtered(lambda x: x.code == 'Adv')
            if advance_line:
                get_amount = self.env['hr.advance'].search([
                    ('employee_id', '=', data.employee_id.id),
                    ('state', '=', 'approve')
                ])
                if get_amount:
                    existing_lines = data.input_line_ids.filtered(lambda x: x.name == 'Adv')  # Get existing loan lines
                    existing_loan_ids = existing_lines.mapped('adv_line_id').ids  # Get IDs of existing loan lines
                    for lines in get_amount:
                        for line in lines.loan_lines:
                            if data.date_from <= line.date <= data.date_to and line.id not in existing_loan_ids:
                                if not line.paid:
                                    amount = line.amount
                                    name = advance_line.id
                                    new_name = self.env['hr.payslip.input.type'].search([('name', '=', 'Advance')])
                                    new_line = {
                                        'input_type_id': new_name.id,
                                        'amount': amount,
                                        'name': 'Adv',
                                        'adv_line_id': line.id
                                    }
                                    data.input_line_ids = [(0, 0, new_line)]
        return super(AdvHrPayslip, self).compute_sheet()

    def input_data_line(self, name, amount, advance):
        """Add loan details to payslip as other input"""
        check_lines = []
        new_name = self.env['hr.payslip.input.type'].search([('name', '=', 'Advance')])
        line = (0, 0, {
            'input_type_id': new_name.id,
            'amount': amount,
            'name': 'Adv',
            'adv_line_id': advance.id
        })
        check_lines.append(line)
        self.input_line_ids = check_lines


class AdvHrPayslipInputType(models.Model):
    """Inherited model for 'hr.payslip.input.type'"""
    _inherit = 'hr.payslip.input.type'

    input_id = fields.Many2one('hr.salary.rule')


class HrSalaryRule(models.Model):
    """New field company_id on salary rule model"""
    _inherit = 'hr.salary.rule'

    company_id = fields.Many2one('res.company', 'Company',
                                 copy=False, readonly=True, help="Comapny",
                                 default=lambda self: self.env.user.company_id)


class AdvHrPayrollStructure(models.Model):
    """New field company_id on 'hr.payroll.structure'"""
    _inherit = 'hr.payroll.structure'

    company_id = fields.Many2one('res.company', 'Company',
                                 copy=False, readonly=True, help="Comapny",
                                 default=lambda self: self.env.user.company_id)


    # access_hr_advance,hr.advance,model_hr_advance,base.group_user,1,1,1,1
# access_hr_advance_line,hr.advance.line,model_hr_advance_line,base.group_user,1,1,1,1
