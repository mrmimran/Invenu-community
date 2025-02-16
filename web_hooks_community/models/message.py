from odoo import models, fields, api, _

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create_enterprise_logs_and_messages(self, payload):
        self.create({
            'res_id': payload.get('res_id'),
            'model': payload.get('model'),
            'body': payload.get('body')
        })
