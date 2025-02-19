# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import UserError
import base64

class MailMessage(models.Model):
    _inherit = 'mail.message'

    is_through_integration = fields.Boolean()
    automation_source_id = fields.Integer()

    def get_chatter_automation_url(self):
        return self.env.company.odoo_chatter_automation_url

    def prepare_attachment_data(self, attachment):
        # Get binary data (either from DB or disk)
        # binary_data = attachment.datas if attachment.datas else open(filestore_path, 'rb').read()
        binary_data = attachment.datas
        # Convert to Base64 for transmission
        encoded_data = base64.b64encode(binary_data).decode('utf-8')
        return {
            "name": attachment.name,
            "store_fname": attachment.name,
            "mimetype": attachment.mimetype,
            "datas": encoded_data
        }

    def send_community_chatter_data(self):
        for rec in self:
            url = rec.get_chatter_automation_url()
            if url:
                attachment_datas = [rec.prepare_attachment_data(att) for att in rec.attachment_ids]
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
                    "automation_source_id": rec.id,
                    "attachment_ids": attachment_datas,
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

    # def write(self, values):
    #     res = super(MailMessage, self).write(values)
    #     if not self.env.context.get('writing_automations', False):
    #         if res.model in ['project.project', 'project.task']:
    #             res.send_enterprise_chatter_data("from_write")
    #     return res


    def get_attachment_ref(self, payload):
        attachment = self.env['ir.attachment'].sudo().create({
            'name': payload.get('name'),
            'store_fname': payload.get('store_fname'),
            'mimetype': payload.get('mimetype'),
            'datas': base64.b64decode(payload.get('datas')),
        })
        return attachment.id


    def receive_enterprise_chatter_data(self, payload):
        attachments = []
        if payload.get('attachment_ids', False):
            attachments = [self.get_attachment_ref(att) for att in payload.get('attachment_ids')]
        if payload['automation_type'] == 'from_create':
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
                    'automation_source_id': payload.get('automation_source_id'),
                    'attachment_ids': attachments,
                    'is_through_integration': True,
                })
        elif payload['automation_type'] == 'from_write':
            msg = self.env['mail.message'].search([('source_id', '=', payload['source_id'])], limit=1)
            if msg:
                msg.with_context(writing_automations=True).sudo().write({
                    "body": payload['body'],
                    "attachment_ids": attachments,
                })

    # payload = json.dumps({
    #     "body": rec.body,
    #     "source_id": rec.id,
    #     "attachment_ids": attachment_datas,
    #     "automation_type": automation_type,
    # })