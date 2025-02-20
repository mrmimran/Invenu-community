import xmlrpc.client
import logging
from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def connect_odoo(self):
        """
        Establishes connection to the Enterprise Odoo instance using XML-RPC.
        All connection parameters for the Enterprise database are fetched from the Odoo instance.
        """

        # sync_url = self.env.company.sync_url
        sync_url = 'https://art-ethereal-advertising-company-staging-main-18283947.dev.odoo.com'
        # sync_db = self.env.company.sync_db
        sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
        # sync_login = self.env.company.sync_login
        sync_login = 'admin@gmail.com'
        # sync_pass = self.env.company.sync_pass
        sync_pass = 'admin'

        # sync_url = self.env.company.sync_url
        # sync_db = self.env.company.sync_db
        # sync_login = self.env.company.sync_login
        # sync_pass = self.env.company.sync_pass

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

    def sync_task_to_enterprise(self, task_data):
        """
        Syncs task data to the Enterprise Odoo instance.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        # Create or update task in the Enterprise Odoo instance
        try:
            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
            # sync_pass = self.env.company.sync_pass
            sync_pass = 'admin'

            enterprise_task_id = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'project.task', 'create',  # Create task in 'project.task' model
                [task_data]
            )

            logging.info(f"Task successfully created in Enterprise Odoo with ID: {enterprise_task_id}")
        except Exception as e:
            logging.error(f"Error creating task in Enterprise Odoo: {e}")
            return False

        return True

    @api.model
    def create(self, values):
        """
        This method overrides the default create method to sync the task data to the Enterprise Odoo.
        """
        # Call the super method to create the record
        res = super(ProjectTask, self).create(values)

        # Prepare the task data to pass to the sync method
        task_data = {
            # 'source_id': res.id,  # Assuming source_id is the task ID in the Enterprise Odoo
            'name': res.name,
            'project_id': res.project_id.source_id,  # Mapping the project ID
            # 'project_id': 27,  # Mapping the project ID
            # 'community_res_users_ids': res.user_ids,  # Mapping the assigned user ID
            'date_deadline': res.date_deadline,
            'description': res.description,
            # You can add other relevant fields for project.task here
        }

        # Call the method to sync the task to Enterprise Odoo
        self.sync_task_to_enterprise(task_data)

        return res
