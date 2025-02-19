# -*- coding: utf-8 -*-

import xmlrpc.client
import logging
from odoo import models, fields, api

class HrLoan(models.Model):
    _inherit = 'hr.loan'

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

    def sync_loan_to_enterprise(self, loan_data):
        """
        Syncs loan data to the Enterprise Odoo instance.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        # Create or update loan in the Enterprise Odoo instance
        try:

            loan_id = enterprise_models.execute_kw(
                self.env.company.sync_db, enterprise_uid, self.env.company.sync_pass,
                'hr.loan', 'create',  # Model name 'hr.loan'
                [loan_data]
            )
            logging.info(f"Loan successfully created in Enterprise Odoo with ID: {loan_id}")
        except Exception as e:
            logging.error(f"Error creating loan in Enterprise Odoo: {e}")
            return False

        return True

    def sync_loan_line_to_enterprise(self, loan_line_data):
        """
        Syncs loan line data to the Enterprise Odoo instance.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        # Create or update loan line in the Enterprise Odoo instance
        try:
            sync_db = 'enterprise-db'  # Replace with actual Enterprise DB if needed
            sync_pass = 'admin'  # Replace with actual Enterprise password

            loan_line_id = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'hr.loan.line', 'create',  # Model name 'hr.loan.line'
                [loan_line_data]
            )
            logging.info(f"Loan line successfully created in Enterprise Odoo with ID: {loan_line_id}")
        except Exception as e:
            logging.error(f"Error creating loan line in Enterprise Odoo: {e}")
            return False

        return True

    @api.model
    def create(self, values):
        """
        This method overrides the default create method to sync the loan data to the Enterprise Odoo.
        """
        # Call the super method to create the loan record
        res = super(HrLoan, self).create(values)

        # Prepare the loan data to pass to the sync method
        loan_data = {
            'employee_id': res.employee_id.source_id,  # Assuming there's a source_id for employee
            # 'loan_type_id': res.loan_type_id.source_id,  # Assuming there's a source_id for loan type
            'loan_amount': res.loan_amount,
            'date': res.date,
            'payment_date': res.payment_date,
            'installment': res.installment,
            'state': res.state,
        }

        # Call the method to sync the loan to the Enterprise Odoo instance
        # self.sync_loan_to_enterprise(loan_data)
        #
        # # Now sync all associated loan lines
        # for line in res.line_ids:
        #     loan_line_data = {
        #         'loan_id': line.loan_id.source_id,  # Assuming there's a source_id for loan
        #         'amount': line.amount,
        #         'date': line.date,
        #         'state': line.state,
        #     }
        #     self.sync_loan_line_to_enterprise(loan_line_data)

        return res
