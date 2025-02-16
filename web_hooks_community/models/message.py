# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests
import json

class MailMessage(models.Model):
    _inherit = 'mail.message'

    def send_community_chatter_data(self):
        for rec in self:
            # url = "http://8.213.43.22:8074/web/hook/5d30af0e-4a3e-4683-9243-b424c6080913"
            url = self.env.company.odoo_chatter_automation_url
            if url:
                payload = json.dumps({
                    "res_id": 25,
                    "model": rec.model,
                    "body": rec.body
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)


    @api.model
    def create(self, values):
        res = super(MailMessage, self).create(values)
        res.send_community_chatter_data()
        return res


    @api.model
    def receive_enterprise_chatter_data(self, payload):
        self.create({
            'res_id': payload.get('res_id'),
            'model': payload.get('model'),
            'body': payload.get('body')
        })
