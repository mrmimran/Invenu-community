# -*- coding: utf-8 -*-

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    sync_url = fields.Char(string='Sync URL')
    # sync_port = fields.Char(string='Sync Port')
    sync_db = fields.Char(string='Sync Database')
    sync_login = fields.Char(string='Sync Login')
    sync_pass = fields.Char(string='Sync Password')

