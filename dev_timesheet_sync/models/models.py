# -*- coding: utf-8 -*-

# from odoo import models, fields, api

import xmlrpc.client
import logging
from datetime import datetime
from odoo import models, fields, api
import base64
import time


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def connect_odoo(self):
        """
        Establishes connection to the Enterprise Odoo instance using XML-RPC.
        All connection parameters for the Enterprise database are fetched from the Odoo instance.
        """

        sync_url = self.env.company.sync_url
        # sync_url = 'https://art-ethereal-advertising-company-staging-main-18283947.dev.odoo.com'
        sync_db = self.env.company.sync_db
        # sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
        sync_login = self.env.company.sync_login
        # sync_login = 'admin@gmail.com'
        sync_pass = self.env.company.sync_pass
        # sync_pass = 'admin'


        enterprise_config = {
            'url': sync_url,
            'db': sync_db,
            'username': sync_login,
            'password': sync_pass
        }

        try:
            # Connect to the Enterprise Odoo using XML-RPC
            common = xmlrpc.client.ServerProxy(f"{enterprise_config['url']}/xmlrpc/2/common")
            enterprise_uid = common.authenticate(enterprise_config['db'], enterprise_config['username'],
                                                 enterprise_config['password'], {})
            if not enterprise_uid:
                raise Exception(f"Failed to authenticate to {enterprise_config['url']}")
            enterprise_models = xmlrpc.client.ServerProxy(f"{enterprise_config['url']}/xmlrpc/2/object")
            logging.info(f"Successfully connected to Enterprise Odoo: {enterprise_config['url']}")
            return enterprise_models, enterprise_uid

        except Exception as e:
            logging.error(f"Error connecting to Enterprise Odoo: {e}")
            return None, None

    def sync_timesheets_to_enterprise(self, timesheet_data):
        """
        Syncs timesheet data to the Enterprise Odoo instance.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        # Create or update timesheet in the Enterprise Odoo instance
        try:
            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
            sync_pass = 'admin'

            enterprise_timesheet_id = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                # self.env.company.sync_db, enterprise_uid, self.env.company.sync_pass,
                'account.analytic.line', 'create',
                [timesheet_data]
            )

            # enterprise_timesheet_id = enterprise_models.execute(
            #     enterprise_uid, 'account.analytic.line', 'create', [timesheet_data]
            # )
            logging.info(f"Timesheet successfully created in Enterprise Odoo with ID: {enterprise_timesheet_id}")
        except Exception as e:
            logging.error(f"Error creating timesheet in Enterprise Odoo: {e}")
            return False

        return True

    @api.model
    def create(self, values):
        """
        This method overrides the default create method to sync the timesheet data to the Enterprise Odoo.
        """
        # Call the super method to create the record
        res = super(AccountAnalyticLine, self).create(values)

        # Prepare the timesheet data to pass to the sync method
        timesheet_data = {
            'project_id': res.project_id.source_id,
            'employee_id': res.employee_id.source_id,
            'task_id': res.task_id.source_id,
            'date': res.date,
            'unit_amount': res.unit_amount,
            'name': res.name,
        }

        # Call the method to sync the timesheet to the Enterprise Odoo instance
        self.sync_timesheets_to_enterprise(timesheet_data)

        return res




