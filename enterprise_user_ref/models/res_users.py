from odoo import models, fields



class ResUsers(models.Model):
    _inherit = 'res.users'

    enterprise_user_reference = fields.Integer()

