from datetime import datetime
from odoo import models, api

class AutomatedActions(models.Model):
    _name = 'automated.actions'
    _description = 'Automated Actions'

    @api.model
    def reset_hr_employee_sent_field(self):
        employees = self.env['hr.employee'].search([('sent', '=', True)])
        employees.write({'sent': False, 'last_sending_date': datetime.now()})
        return True
