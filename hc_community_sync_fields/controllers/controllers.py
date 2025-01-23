# -*- coding: utf-8 -*-
# from odoo import http


# class OdooApiIntegration(http.Controller):
#     @http.route('/odoo_api_integration/odoo_api_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_api_integration/odoo_api_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_api_integration.listing', {
#             'root': '/odoo_api_integration/odoo_api_integration',
#             'objects': http.request.env['odoo_api_integration.odoo_api_integration'].search([]),
#         })

#     @http.route('/odoo_api_integration/odoo_api_integration/objects/<model("odoo_api_integration.odoo_api_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_api_integration.object', {
#             'object': obj
#         })
