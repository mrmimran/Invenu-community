# -*- coding: utf-8 -*-
# from odoo import http


# class SyncModule(http.Controller):
#     @http.route('/sync_module/sync_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sync_module/sync_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sync_module.listing', {
#             'root': '/sync_module/sync_module',
#             'objects': http.request.env['sync_module.sync_module'].search([]),
#         })

#     @http.route('/sync_module/sync_module/objects/<model("sync_module.sync_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sync_module.object', {
#             'object': obj
#         })
