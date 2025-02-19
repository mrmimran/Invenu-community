# -*- coding: utf-8 -*-

import xmlrpc.client
import logging
from odoo import models, fields, api

class SalaryAdvance(models.Model):
    _inherit = 'salary.advance'

    def connect_odoo(self):
        """
        Establishes connection to the Enterprise Odoo instance using XML-RPC.
        All connection parameters for the Enterprise database are fetched from the Odoo instance.
        """
        # Fetch connection parameters from the current company
        sync_url = self.env.company.sync_url
        sync_db = self.env.company.sync_db
        sync_login = self.env.company.sync_login
        sync_pass = self.env.company.sync_pass

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

    def sync_salary_advance_to_enterprise(self, advance_data):
        """
        Syncs salary advance data to the Enterprise Odoo instance.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        # Create or update salary advance in the Enterprise Odoo instance
        try:
            advance_id = enterprise_models.execute_kw(
                self.env.company.sync_db, enterprise_uid, self.env.company.sync_pass,
                'hr.advance', 'create',  # Model name 'salary.advance'
                [advance_data]
            )
            logging.info(f"Salary advance successfully created in Enterprise Odoo with ID: {advance_id}")
        except Exception as e:
            logging.error(f"Error creating salary advance in Enterprise Odoo: {e}")
            return False

        return True

    # def sync_salary_advance_line_to_enterprise(self, advance_line_data):
    #     """
    #     Syncs salary advance line data to the Enterprise Odoo instance.
    #     """
    #     enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo
    #
    #     if not enterprise_models:
    #         logging.error("Unable to connect to Enterprise Odoo.")
    #         return False
    #
    #     # Create or update salary advance line in the Enterprise Odoo instance
    #     try:
    #         advance_line_id = enterprise_models.execute_kw(
    #             self.env.company.sync_db, enterprise_uid, self.env.company.sync_pass,
    #             'salary.advance.line', 'create',  # Model name 'salary.advance.line'
    #             [advance_line_data]
    #         )
    #         logging.info(f"Salary advance line successfully created in Enterprise Odoo with ID: {advance_line_id}")
    #     except Exception as e:
    #         logging.error(f"Error creating salary advance line in Enterprise Odoo: {e}")
    #         return False
    #
    #     return True

    @api.model
    def create(self, values):
        """
        This method overrides the default create method to sync the salary advance data to the Enterprise Odoo.
        """
        # Call the super method to create the salary advance record
        res = super(SalaryAdvance, self).create(values)

        # Prepare the salary advance data to pass to the sync method
        advance_data = {
            'employee_id': res.employee_id.source_id,  # Assuming there's a source_id for employee
            'loan_amount': res.advance,
            'date': res.date,
            'state': res.state,
        }

        # Call the method to sync the salary advance to the Enterprise Odoo instance
        self.sync_salary_advance_to_enterprise(advance_data)

        # # Now sync all associated salary advance lines
        # for line in res.line_ids:
        #     advance_line_data = {
        #         'advance_id': line.advance_id.id,  # Assuming there's a source_id for salary advance
        #         'amount': line.amount,
        #         'date': line.date,
        #         'state': line.state,
        #     }
        #     self.sync_salary_advance_line_to_enterprise(advance_line_data)

        return res
