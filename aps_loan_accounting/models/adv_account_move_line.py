# -*- coding: utf-8 -*-

from odoo import models, api, fields


class AdvAccountMoveLine(models.Model):
    _inherit = "account.move.line"

    adv_id = fields.Many2one('hr.advance', 'Advance Id')
