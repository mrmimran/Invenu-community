# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
import json
from datetime import datetime


class MailMessage(models.Model):
    _inherit = 'mail.message'

    is_through_integration = fields.Boolean()


    def send_community_chatter_data(self):
        for rec in self:
            # url = "http://8.213.43.22:8074/web/hook/5d30af0e-4a3e-4683-9243-b424c6080913"
            url = self.env.company.odoo_chatter_automation_url
            if url:
                payload = json.dumps({
                    "res_id": 8,
                    "model": rec.model,
                    "body": rec.body,
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)


    @api.model
    def create(self, values):
        res = super(MailMessage, self).create(values)
        if not res.is_through_integration:
            res.send_community_chatter_data()
        return res


    # @api.model
    def receive_enterprise_chatter_data(self, payload):
        res_id = self.env['project.task'].search([('source_id', '=', payload['res_id'])], limit=1)

        if res_id:

            create_uid = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('create_uid'))], limit=1)
            write_uid = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('write_uid'))], limit=1)
            author_id = self.env['res.users'].search([('enterprise_user_reference', '=', payload.get('author_id'))], limit=1)

            self.env['mail.message'].sudo().create({
                'message_type': payload.get('message_type'),
                'record_name': payload.get('record_name'),
                'subject': payload.get('subject'),

                'create_uid': create_uid.id if create_uid else False,
                'write_uid': write_uid.id if write_uid else False,
                'author_id': author_id.partner_id.id if author_id else False,

                'res_id': res_id.id,
                'model': payload.get('model'),
                'body': payload.get('body'),
                'is_through_integration': True
            })
