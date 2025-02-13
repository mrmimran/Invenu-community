from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    sent = fields.Boolean(string='Sent', default=False, readonly=True, store=True)
    sync = fields.Boolean(string='Sync', default=False)


