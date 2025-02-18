# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, tools, _
from odoo.addons.base.models.ir_attachment import IrAttachment as BaseIrAttachment
import base64




class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    is_through_integration = fields.Boolean()


@api.model_create_multi
def create(self, vals_lists):
    for vals_list in vals_lists:
        if vals_list[0].get('is_through_integration', False):
            return super().create(vals_list)
        else:
            record_tuple_set = set()
            vals_list = [{
                key: value
                for key, value
                in vals.items()
                if key not in ('file_size', 'checksum', 'store_fname')
            } for vals in vals_list]
            for values in vals_list:
                values = self._check_contents(values)
                raw, datas = values.pop('raw', None), values.pop('datas', None)
                if raw or datas:
                    if isinstance(raw, str):
                        raw = raw.encode()
                    values.update(self._get_datas_related_values(
                        raw or base64.b64decode(datas or b''),
                        values['mimetype']
                    ))
                record_tuple = (values.get('res_model'), values.get('res_id'))
                record_tuple_set.add(record_tuple)
            Attachments = self.browse()
            for res_model, res_id in record_tuple_set:
                Attachments.check('create', values={'res_model':res_model, 'res_id':res_id})
            return super(BaseIrAttachment, self).create(vals_list)
BaseIrAttachment.create = IrAttachment.create
