# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, tools, _
from odoo.addons.base.models.ir_attachment import IrAttachment as BaseIrAttachment
import base64
import json


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    is_through_integration = fields.Boolean()

    def create_data(self, payload):
        self.env['ir.attachment'].sudo().create({
            'name': payload.get('name'),
            'store_fname': payload.get('store_fname'),
            'mimetype': payload.get('mimetype'),
            'datas': base64.b64decode(payload.get('datas')),
        })

