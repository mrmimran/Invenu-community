from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    odoo_chatter_automation_url = fields.Char(string='Chatter URL')
