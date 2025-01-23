# -*- coding: utf-8 -*-
# from odoo import http


# class ErpSync(http.Controller):
#     @http.route('/erp_sync/erp_sync', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/erp_sync/erp_sync/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('erp_sync.listing', {
#             'root': '/erp_sync/erp_sync',
#             'objects': http.request.env['erp_sync.erp_sync'].search([]),
#         })

#     @http.route('/erp_sync/erp_sync/objects/<model("erp_sync.erp_sync"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('erp_sync.object', {
#             'object': obj
#         })
