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
        # # sync_login = self.env.company.sync_login
        sync_login = 'admin@gmail.com'
        # # sync_pass = self.env.company.sync_pass
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

    # def sync_task_to_enterprise(self, task_data):
    def sync_task_to_enterprise(self):
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
            # sync_db = self.env.company.sync_db

            # sync_pass = self.env.company.sync_pass
            sync_pass = 'admin'
            user_ids = self.user_ids.ids
            community_res_users_ids = self.search_user_in_community(user_ids)
            formatted_user_ids = [(6, 0, community_res_users_ids)]  # 6 means "replace with these IDs"

            task_data = {
                # 'source_id': self.id,  # Assuming source_id is the task ID in the Enterprise Odoo
                'source_id': self.id,  # Assuming source_id is the task ID in the Enterprise Odoo
                "name": self.name,
                'project_id': self.project_id.source_id,
                # 'project_id': 27,
                'date_deadline': self.date_deadline,
                'description': self.description,
                'allocated_hours': self.allocated_hours,
                'community_res_users_ids': formatted_user_ids,
            }

            source_id = self.id
            #source_id = 295
            # Search for the existing task in Enterprise Odoo
            task_id = self.search_task_in_enterprise(source_id)
            if not task_id:
                enterprise_task_id = enterprise_models.execute_kw(
                    sync_db, enterprise_uid, sync_pass,
                    'project.task', 'create',  # Create task in 'project.task' model
                    [task_data]
                )
            else:
                self.update_task_in_enterprise(task_id, task_data)
            logging.info(f"Task successfully created in Enterprise Odoo with ID: {enterprise_task_id}")
        except Exception as e:
            logging.error(f"Error creating task in Enterprise Odoo: {e}")
            return False

        return True

    @api.model
    # def create(self, values):
    #     """
    #     This method overrides the default create method to sync the task data to the Enterprise Odoo.
    #     """
    #     # Call the super method to create the record
    #     res = super(ProjectTask, self).create(values)
    #
    #     # Prepare the task data to pass to the sync method
    #     task_data = {
    #         'source_id': res.id,  # Assuming source_id is the task ID in the Enterprise Odoo
    #         'name': res.name,
    #         # 'project_id': res.project_id.source_id,  # Mapping the project ID
    #         # 'project_id': 27,  # Mapping the project ID
    #         # 'community_res_users_ids': res.user_ids,  # Mapping the assigned user ID
    #         'date_deadline': res.date_deadline,
    #         'description': res.description,
    #         'allocated_hours': res.allocated_hours,
    #         # You can add other relevant fields for project.task here
    #     }
    #
    #     # Call the method to sync the task to Enterprise Odoo
    #     # self.sync_task_to_enterprise(task_data)
    #     # res.sync_task_to_enterprise(task_data)
    #
    #     return res

    # def write(self, vals):
    #     """
    #     This method overrides the default write method to sync the task data to the Enterprise Odoo.
    #     If the task exists in the Enterprise Odoo system, it updates it; otherwise, it creates a new task.
    #     """
    #
    #     res = super().write(vals)
    #     # Get the source_id from the vals or fallback to self.source_id
    #     source_id = vals.get('id') or self.id
    #     # source_id = 295
    #
    #     # Search for the existing task in Enterprise Odoo
    #     # task_id = self.search_task_in_enterprise(source_id)
    #
    #     # if task_id:
    #     if source_id:
    #         pass
    #         # If the task exists, update it in the Enterprise Odoo system
    #         # self.update_task_in_enterprise(task_id, vals)
    #     else:
    #         pass
    #         # If the task doesn't exist, create a new task in Enterprise Odoo
    #         # return self.create_task_in_enterprise(vals)
    #     return res

    def search_task_in_enterprise(self, source_id):
        """
        Searches for an existing task in the Enterprise Odoo instance based on the given source_id.
        Returns the task ID if found, or False if not found.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        try:
            # Get the database and password for connection
            # sync_db = self.env.company.sync_db
            # sync_pass = self.env.company.sync_pass

            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
            # sync_db = self.env.company.sync_db

            # sync_pass = self.env.company.sync_pass
            sync_pass = 'admin'

            # Search for the task by source_id
            existing_task_ids = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'project.task', 'search',
                [[('source_id', '=', source_id)]]  # Searching by source_id
            )

            if existing_task_ids:
                return existing_task_ids[0]  # Return the first task ID if found
            else:
                logging.info(f"No task found with source_id {source_id}")
                return False

        except Exception as e:
            logging.error(f"Error searching for task in Enterprise Odoo: {e}")
            return False

    def search_user_in_community(self, source_id):
        """
        Searches for an existing user in the Community Odoo instance based on the given user_id.
        Returns the user ID if found, or False if not found.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Odoo.")
            return False

        try:
            # Get the database and password for connection
            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'  # Example database
            sync_pass = 'admin'  # Example password

            # Search for the user by user_id
            existing_user_ids = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'community.res.users', 'search',
                [[('source_id', 'in', source_id)]]  # Searching by user_id
            )

            if existing_user_ids:
                return existing_user_ids  # Return the first user ID if found
            else:
                logging.info(f"No user found with user_id {source_id}")
                return False

        except Exception as e:
            logging.error(f"Error searching for user in Odoo: {e}")
            return False

    def update_task_in_enterprise(self, task_id, task_data):
        """
        Updates the task in the Enterprise Odoo instance with the given task data.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Enterprise Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Enterprise Odoo.")
            return False

        try:
            # Get the database and password for connection
            # sync_db = self.env.company.sync_db
            # sync_pass = self.env.company.sync_pass
            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'
            # sync_db = self.env.company.sync_db

            # sync_pass = self.env.company.sync_pass
            sync_pass = 'admin'

            # Update the existing task
            enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'project.task', 'write',
                [task_id, task_data]  # Update task with the new data
            )

            logging.info(f"Task with ID {task_id} successfully updated in Enterprise Odoo.")

        except Exception as e:
            logging.error(f"Error updating task in Enterprise Odoo: {e}")
            return False

        return True

    def synchronize_timesheet_data(self):
        """
        Calls the search_timesheet_in_enterprise method to either retrieve existing timesheet data
        or prepare new timesheet data for synchronization.
        """
        # Call the search_timesheet_in_enterprise method to get existing or prepare new timesheet data
        # prepared_data = self.search_timesheet_in_enterprise(source_id)
        prepared_data = self.prepare_timesheet_data()

        if not prepared_data:
            logging.error("No timesheet data available for synchronization.")
            return False

        # Now you can use the prepared data, e.g., send it to Odoo for synchronization
        for timesheet_entry in prepared_data:
            # Call the search_timesheet_in_enterprise method for each timesheet_entry
            # passing the task_id (source_id) of the timesheet
            timesheet_id = timesheet_entry.get('task_id')  # Adjust if needed based on the structure of timesheet_entry
            source_id = timesheet_entry['source_id']

            # Call search_timesheet_in_enterprise for each timesheet entry
            existing_timesheet = self.search_timesheet_in_enterprise(source_id)

            if existing_timesheet:
                # If the timesheet is found, update the existing timesheet in Odoo
                logging.info(f"Synchronizing existing timesheet for task {timesheet_entry['task_id']}")

                # You can modify this logic to update specific fields in the existing timesheet
                enterprise_models, enterprise_uid = self.connect_odoo()
                sync_db = 'art-ethereal-advertising-company-staging-main-18283947'  # Example database
                sync_pass = 'admin'  # Example password

                # Ensure the existing_timesheet is a list of IDs and extract the first ID
                timesheet_id = existing_timesheet[0] if isinstance(existing_timesheet, list) else existing_timesheet

                # Now perform the update operation
                enterprise_models.execute_kw(
                    sync_db, enterprise_uid, sync_pass,
                    'account.analytic.line', 'write',
                    [[timesheet_id], {
                        'unit_amount': timesheet_entry.get('unit_amount'),  # Update hours worked
                        'name': timesheet_entry.get('name'),  # Update task description
                        'date': timesheet_entry.get('date')  # Update the date if necessary
                    }]
                )
            else:
                # If no timesheet is found, create a new timesheet in Odoo
                logging.info(
                    f"No existing timesheet found for task {timesheet_entry['task_id']}. Creating new timesheet.")

                # Create new timesheet entry
                enterprise_models, enterprise_uid = self.connect_odoo()
                sync_db = 'art-ethereal-advertising-company-staging-main-18283947'  # Example database
                sync_pass = 'admin'  # Example password

                # Prepare data for creating a new timesheet
                new_timesheet_data = {

                    'project_id': timesheet_entry['project_id'],  # Example: Pass task_id (source_id)
                    'task_id': timesheet_entry['task_id'],  # Example: Pass task_id (source_id)
                    'employee_id': timesheet_entry['employee_id'],  # Employee who logged the time
                    'date': timesheet_entry['date'],  # Date of the timesheet entry
                    'unit_amount': timesheet_entry['unit_amount'],  # Hours worked
                    'name': timesheet_entry['name'],  # Description of the work done
                    'source_id': timesheet_entry['source_id'],  # Description of the work done
                }

                # Create a new timesheet entry in Odoo
                new_timesheet_id = enterprise_models.execute_kw(
                    sync_db, enterprise_uid, sync_pass,
                    'account.analytic.line', 'create',
                    [new_timesheet_data]
                )
                logging.info(f"New timesheet created with ID {new_timesheet_id}.")

            return prepared_data  # Return the prepared data, which might have been synchronized or updated

        # You could also return the prepared data if needed
        return prepared_data

    def prepare_timesheet_data(self):
        """
        Prepares the timesheet data for synchronization with Enterprise Odoo.
        """
        # Prepare the timesheet data based on the current task and timesheet entry
        timesheet_ids = self.timesheet_ids
        timesheet_data_list = []  # To hold the prepared timesheet data
        source_id = self.id
        task_id = self.search_task_in_enterprise(source_id)

        for timesheet_line in timesheet_ids:
            # Assuming each timesheet_line is an object containing the necessary data

            timesheet_data = {
                # 'task_id': self.source_id,  # Assuming source_id is the task ID in Enterprise Odoo
                'project_id': self.project_id.source_id,
                # 'project_id': 27,
                'task_id': task_id,  # Assuming source_id is the task ID in Enterprise Odoo
                # 'task_id': 378,  # Assuming source_id is the task ID in Enterprise Odoo
                # 'task_id': self.id,  # Assuming source_id is the task ID in Enterprise Odoo
                'employee_id': timesheet_line.employee_id.source_id,  # Employee who logged the time
                # 'employee_id': 72,  # Employee who logged the time
                'date': timesheet_line.date,  # Date of the timesheet entry
                'unit_amount': timesheet_line.unit_amount,  # Hours worked
                'name': timesheet_line.name,  # Description of the work done
                'source_id': self.id
            }
            timesheet_data_list.append(timesheet_data)  # Add the data to the list

        return timesheet_data_list  # Return the list of timesheet data

    def search_timesheet_in_enterprise(self, source_id):
        """
        Searches for existing timesheet entries in the Enterprise Odoo instance based on the given source_id (task_id).
        If the timesheet exists, returns the existing timesheet entries.
        If not, prepares new timesheet data by calling the prepare_timesheet_data method.
        """
        enterprise_models, enterprise_uid = self.connect_odoo()  # Connect to Odoo

        if not enterprise_models:
            logging.error("Unable to connect to Odoo.")
            return False

        try:
            # Get the database and password for connection
            sync_db = 'art-ethereal-advertising-company-staging-main-18283947'  # Example database
            sync_pass = 'admin'  # Example password

            # Search for the timesheet entries by task_id (source_id) in the Enterprise Odoo instance
            existing_timesheet_ids = enterprise_models.execute_kw(
                sync_db, enterprise_uid, sync_pass,
                'account.analytic.line', 'search',
                [[('source_id', '=', source_id)]]  # Searching by task_id (source_id)
            )

            # If timesheets are found, return the existing records
            logging.info(f"Found existing timesheet entries for task_id {source_id}")
            return existing_timesheet_ids  # You could also fetch more details if needed

        except Exception as e:
            logging.error(f"Error searching for timesheet in Enterprise Odoo: {e}")
            return False



