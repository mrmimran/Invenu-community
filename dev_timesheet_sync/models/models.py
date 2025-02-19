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


        # Define the connection parameters for the Enterprise Odoo instance
        # enterprise_config = {
        #     'url': 'https://testerp.invenu.com',  # Update with your Enterprise Odoo URL
        #     'db': 'dev-invenu-db-db',  # Update with your Enterprise Odoo Database Name
        #     'username': 'admin@gmail.com',  # Update with the Enterprise username
        #     'password': 'admin'  # Update with the Enterprise password
        # }
        enterprise_config = {
            'url': self.env.company.sync_url,
            'db': self.env.company.sync_db,
            'username': self.env.company.sync_login,
            'password': self.env.company.sync_pass
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
            db = "dev-invenu-db-db"
            password = "admin"
            enterprise_timesheet_id = enterprise_models.execute_kw(
                # self.env.company.sync_db, enterprise_uid, self.env.company.sync_pass,
                db, enterprise_uid, password,
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
            # 'task_id': res.task_id.id,
            # 'project_id': 22,
            'project_id': res.project_id.source_id,
            'task_id': res.task_id.source_id,
            'date': res.date,
            'unit_amount': res.unit_amount,
            'name': res.name,
        }

        # Call the method to sync the timesheet to the Enterprise Odoo instance
        self.sync_timesheets_to_enterprise(timesheet_data)

        return res




