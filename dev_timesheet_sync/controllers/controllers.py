# -*- coding: utf-8 -*-
# from odoo import http


# class DevTimesheetSync(http.Controller):
#     @http.route('/dev_timesheet_sync/dev_timesheet_sync', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dev_timesheet_sync/dev_timesheet_sync/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dev_timesheet_sync.listing', {
#             'root': '/dev_timesheet_sync/dev_timesheet_sync',
#             'objects': http.request.env['dev_timesheet_sync.dev_timesheet_sync'].search([]),
#         })

#     @http.route('/dev_timesheet_sync/dev_timesheet_sync/objects/<model("dev_timesheet_sync.dev_timesheet_sync"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dev_timesheet_sync.object', {
#             'object': obj
#         })

