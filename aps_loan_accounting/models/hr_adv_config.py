# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdvanceConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    advance_approve = fields.Boolean(default=False, string="Approval from Accounting Department",
                                  help="Advance Approval from account manager")

    @api.model
    def get_values(self):
        res = super(AdvanceConfig, self).get_values()
        res.update(
            advance_approve=self.env['ir.config_parameter'].sudo().get_param('account.advance_approve')
        )
        print(res, 'resssssss')
        return res


    def set_values(self):
        super(AdvanceConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('account.advance_approve', self.advance_approve)

