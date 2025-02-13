from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)
    employee_project_manager = fields.Many2one('hr.employee', string='Employee Project Manager', required=False)

class ProjectProjectStage(models.Model):
    _inherit = 'project.project.stage'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)
    employee_project_manager = fields.Many2one('hr.employee', string='Employee Project Manager', required=False)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class HVTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


    last_sending_date = fields.Datetime(string='Last Sending Date', readonly=True, store=True)
    sent = fields.Boolean(string='Sent', default=False, readonly=True, store=True)
    sync = fields.Boolean(string='Sync', default=False)


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class HrJob(models.Model):
    _inherit = 'hr.job'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class HRBankInherit(models.Model):
    _inherit = 'res.bank'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class RESPartnerBankInherit(models.Model):
    _inherit = 'res.partner.bank'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class AccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

class HrContract(models.Model):
    _inherit = 'hr.contract'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure.type'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


# class ResourceCalendarIInherit(models.Model):
#     _inherit = 'resource.calendar'
#
#     # Fields for synchronization
#     source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
#     last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    sent = fields.Boolean(string='Sent', default=False, readonly=True, store=True)
    sync = fields.Boolean(string='Sync', default=False)

