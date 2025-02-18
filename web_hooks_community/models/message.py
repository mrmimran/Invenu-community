# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
import json
from datetime import datetime
from odoo.exceptions import UserError


class MailMessage(models.Model):
    _inherit = 'mail.message'

    is_through_integration = fields.Boolean()
    def send_community_chatter_data(self):
        for rec in self:
            url = self.env.company.odoo_chatter_automation_url
            if url:
                res = self.env['project.task'].search([('id', '=', rec.res_id)])
                payload = json.dumps({
                    'message_type': rec.message_type,
                    'record_name': rec.record_name,
                    'subject': rec.subject,
                    'create_uid': rec.create_uid.id,
                    'write_uid': rec.write_uid.id,
                    'author_id': rec.author_id.user_ids.ids[0] if rec.author_id.user_ids else False,
                    "res_id": res.source_id,
                    "model": rec.model,
                    "body": rec.author_id.name + rec.body,
                })
                # raise UserError(payload)
                headers = {'Content-Type': 'application/json'}
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)


    @api.model
    def create(self, values):
        res = super(MailMessage, self).create(values)
        if not res.is_through_integration and res.model == 'project.task':
            res.send_community_chatter_data()
        return res


    def receive_enterprise_chatter_data(self, payload):
        res_id = self.env['project.task'].search([('source_id', '=', payload['res_id'])], limit=1)

        if res_id:

            create_uid = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('create_uid'))], limit=1)
            write_uid = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('write_uid'))], limit=1)
            author_id = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('author_id'))], limit=1)

            # Create the message
            message = self.env['mail.message'].sudo().create({
                'message_type': payload.get('message_type'),
                'record_name': payload.get('record_name'),
                'subject': payload.get('subject'),
                'create_uid': create_uid.id if create_uid else False,
                'write_uid': write_uid.id if write_uid else False,
                'author_id': author_id.partner_id.id if author_id else False,
                'res_id': res_id.id,
                'model': payload.get('model'),
                'body': payload.get('body'),
                # 'attachment_ids': payload.get('attachment_ids'),
                'is_through_integration': True
            })

            attachments = message.attachment_ids
            if attachments:
               for att in attachments:
                   attachment = self.env['ir.attachment'].sudo().create({
                       'name': att.name,
                       'type': att.type,
                       'datas': att.datas,  # base64 encoding the PDF content
                       'store_fname': att.store_fname,  # Filename that the user sees
                       'res_model': att.res_model,  # The model to which the attachment is linked
                       'res_id': att.res_id,  # The ID of the resource to which the attachment is linked
                       'mimetype': att.mimetype,  # MIME type for PDF files
                   })
                   raise UserError(payload)






    # def write(self, vals):
    #     res = super().write(vals)
    #     attachment = self.env['ir.attachment'].sudo().create({
    #         'name': self.attachment_ids.name,
    #         'type': self.attachment_ids.type,
    #         'datas': self.attachment_ids.datas,  # base64 encoding the PDF content
    #         'store_fname': self.attachment_ids.store_fname,  # Filename that the user sees
    #         'res_model': self.attachment_ids.res_model,  # The model to which the attachment is linked
    #         'res_id': self.attachment_ids.res_id,  # The ID of the resource to which the attachment is linked
    #         'mimetype': self.attachment_ids.mimetype,  # MIME type for PDF files
    #     })
    #
    #     return res


