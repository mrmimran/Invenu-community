# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
import json

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
        # payload = json.loads(payload)
        res_id = self.env['project.task'].search([('source_id', '=', payload['res_id'])], limit=1)
        if res_id:
            self.create({
                # 'date': payload.get('date'),
                'message_type': payload.get('message_type'),
                'record_name': payload.get('record_name'),
                'subject': payload.get('subject'),

                'write_uid': payload.get('write_uid'),
                'create_uid': payload.get('create_uid'),
                'author_id': payload.get('author_id'),

                'res_id': res_id.id,
                'model': payload.get('model'),
                'body': payload.get('body'),
                'is_through_integration': True
            })


    # @api.model
    # def receive_enterprise_chatter_data(self, payload):
    #     # payload = json.loads(payload)
    #     self.create({
    #         'res_id': payload.get('res_id'),
    #         'model': payload.get('model'),
    #         'body': payload.get('body'),
    #         'is_through_integration': True
    #     })
