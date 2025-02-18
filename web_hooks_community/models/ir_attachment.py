from odoo import models
import base64


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'


    # def create_attachment_from_pdf(self, model, res_id, filename, report_name):
    def create_attachment_from_pdf(self):
        """
        Creates an attachment from a report and links it to the specified resource.

        :param model: The model where the attachment is linked (e.g., 'account.invoice').
        :param res_id: The ID of the resource (e.g., invoice ID).
        :param filename: The name of the attachment file.
        :param report_name: The name of the report to generate (e.g., 'account.report_invoice').
        :return: The created attachment.
        """

        res_id = 87
        # Generate the PDF report (or any other file) from the given model and report name
        pdf = self.env['sale.order'].sudo().get_pdf([res_id], report_name)

        filename = 'test'
        model = 'project.task'
        res_id = 31

        # Create the attachment
        attachment = self.env['ir.attachment'].sudo().create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf),  # base64 encoding the PDF content
            'datas_fname': filename,  # Filename that the user sees
            'res_model': model,  # The model to which the attachment is linked
            'res_id': res_id,  # The ID of the resource to which the attachment is linked
            'mimetype': 'application/x-pdf',  # MIME type for PDF files
        })

        return attachment

    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     self.create_attachment_from_pdf()
    #     return res




# class ProjectTaskInherit(models.Model):
#     _inherit = 'project.task'
#
#
#     def write(self, vals):
#         res = super().write(vals)
#
#         attachment = self.env['ir.attachment'].sudo().create({
#             'name': filename,
#             'type': 'binary',
#             'datas': base64.b64encode(pdf),  # base64 encoding the PDF content
#             'datas_fname': filename,  # Filename that the user sees
#             'res_model': model,  # The model to which the attachment is linked
#             'res_id': res_id,  # The ID of the resource to which the attachment is linked
#             'mimetype': 'application/x-pdf',  # MIME type for PDF files
#         })
#
#         return res
