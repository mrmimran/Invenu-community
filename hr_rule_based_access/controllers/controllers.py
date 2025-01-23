# -*- coding: utf-8 -*-
# from odoo import http


# class HrRuleBasedAccess(http.Controller):
#     @http.route('/hr_rule_based_access/hr_rule_based_access', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_rule_based_access/hr_rule_based_access/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_rule_based_access.listing', {
#             'root': '/hr_rule_based_access/hr_rule_based_access',
#             'objects': http.request.env['hr_rule_based_access.hr_rule_based_access'].search([]),
#         })

#     @http.route('/hr_rule_based_access/hr_rule_based_access/objects/<model("hr_rule_based_access.hr_rule_based_access"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_rule_based_access.object', {
#             'object': obj
#         })

