# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json
from datetime import datetime
import datetime


# Define the global URL for the external API
BASE_URL = 'http://34.220.171.21:8069'
EMP_API_ENDPOINT = '/api/employees'
AUT_API_ENDPOINT = '/web/session/authenticate'
JOB_API_ENDPOINT = '/api/jobs'
DEP_API_ENDPOINT = '/api/departments'
PRO_API_ENDPOINT = '/api/project'
BNK_API_ENDPOINT = '/api/bank'
BNK_ACC_API_ENDPOINT = '/api/bank_account'
BNK_ACC_ANA_API_ENDPOINT = '/api/account_analytic'

def make_api_request(url, payload, headers):
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_session_id():
    url = BASE_URL + AUT_API_ENDPOINT

    payload = json.dumps({
        "jsonrpc": "2.0",
        "params": {
            "db": "idea-to-life",
            "login": "admin",
            "password": "admin"
        }
    })
    headers = {
        'Content-Type': 'application/json',
        # 'Cookie': 'session_id=527ac2aa0b1af4fd399639c6c4336fd7bb5fe8cc'
    }

    response = make_api_request(url, payload, headers)

    if response:
        session_id = response.cookies.get('session_id')
        return session_id
    else:
        return None


# Rest of the code remains unchanged...


class ResUsers(models.Model):
    _inherit = 'res.users'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def create_projects(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + PRO_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()

            if response:
                try:
                    projects_list = response_data["data"]["projects"]

                    for project_data in projects_list:
                        source_id = project_data.get('id')

                        # Check if the project already exists in the system
                        existing_project = self.env['project.project'].search([('source_id', '=', source_id)], limit=1)

                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': source_id,
                            'name': project_data.get('name'),
                            'label_tasks': project_data.get('label_tasks'),
                            'date_start': project_data.get('date_start'),
                            # Add more fields as needed
                        }

                        # Handle partner_id field
                        partner_id = project_data.get('partner_id')
                        if partner_id:
                            # Check if the partner with the given source_id already exists in the system
                            existing_partner = self.env['res.partner'].search([('source_id', '=', partner_id)], limit=1)
                            if existing_partner:
                                record_data['partner_id'] = existing_partner.id
                            else:
                                # Create a new partner record and link it to the project
                                new_partner = self.env['res.partner'].create({'source_id': partner_id})
                                record_data['partner_id'] = new_partner.id

                        # Handle user_id field
                        user_id = project_data.get('user_id')
                        if user_id:
                            # Check if the user with the given source_id already exists in the system
                            existing_user = self.env['res.users'].search([('source_id', '=', user_id)], limit=1)
                            if existing_user:
                                record_data['user_id'] = existing_user.id
                            else:
                                # Create a new user record and link it to the project
                                new_user = self.env['res.users'].create({'source_id': user_id})
                                record_data['user_id'] = new_user.id

                        # Handle tag_ids field (many2many)
                        tag_ids = project_data.get('tag_ids')
                        if tag_ids:
                            # Check if the tags with the given source_ids already exist in the system
                            existing_tags = self.env['project.tags'].search([('source_id', 'in', tag_ids)])
                            record_data['tag_ids'] = [(6, 0, existing_tags.ids)]

                        if existing_project:
                            # Update the existing record with the new data
                            existing_project.write(record_data)
                        else:
                            # Create a new record
                            self.env['project.project'].create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    # Your existing code for fetch_employees_from_api and create_job_positions methods...

    def create_departments(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + DEP_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()

            if response:
                try:
                    departments_list = response_data["data"]["departments"]

                    for department_data in departments_list:
                        source_id = department_data.get('id')

                        # Check if the department already exists in the system
                        existing_department = self.env['hr.department'].search([('source_id', '=', source_id)], limit=1)

                        # Check if the manager already exists in the system
                        manager_id = self.env['hr.employee'].search([('manager_id', '=', department_data.get('manager_id'))], limit=1)

                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': department_data.get('id'),
                            'name': department_data.get('name'),
                            # Add more fields as needed
                        }

                        if existing_department:
                            # Update the existing record with the new data
                            existing_department.write(record_data)
                        else:
                            # Create a new record
                            self.env['hr.department'].create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")


class HrJob(models.Model):
    _inherit = 'hr.job'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def create_job_positions(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + JOB_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()

            if response:
                try:
                    jobs_list = response_data["data"]["jobs"]

                    for job_data in jobs_list:
                        source_id = job_data.get('id')

                        # Check if the job position already exists in the system
                        existing_job_position = self.env['hr.job'].search([('source_id', '=', source_id)], limit=1)

                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': job_data.get('id'),
                            'name': job_data.get('name'),
                            # 'description': job_data.get('description'),
                            # Add more fields as needed
                        }

                        if existing_job_position:
                            # Update the existing record with the new data
                            existing_job_position.write(record_data)
                        else:
                            # Create a new record
                            self.env['hr.job'].create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def fetch_employees_from_api(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + EMP_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()

            if response:
                try:
                    employees_list = response_data["data"]["employees"]

                    for employee_data in employees_list:
                        source_id = employee_data.get('id')

                        # Check if a record with the same source_id already exists
                        existing_record = self.search([('source_id', '=', source_id)], limit=1)

                        # Check if a department record with the same source_id already exists
                        department_id = self.env['hr.department'].search([('source_id', '=', employee_data.get('department_id'))], limit=1).id

                        # Check if a job record with the same source_id already exists
                        job_id = self.env['hr.job'].search([('source_id', '=', employee_data.get('job_id'))], limit=1).id

                        # Check if a parent_id record with the same source_id already exists
                        parent_id = self.env['hr.employee'].search([('source_id', '=', employee_data.get('parent_id'))],limit=1).id

                        # Check if a parent_id record with the same source_id already exists
                        coach_id = self.env['hr.employee'].search([('source_id', '=', employee_data.get('coach_id'))],limit=1).id


                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': employee_data.get('id'),
                            'name': employee_data.get('name'),
                            'department_id': department_id,
                            'parent_id': parent_id if parent_id else False,
                            'coach_id': coach_id if coach_id else False,
                            'job_id': job_id,
                            'work_email': employee_data.get('work_email'),
                            'mobile_phone': employee_data.get('mobile_phone'),
                            'work_phone': employee_data.get('work_phone'),
                            'tz': employee_data.get('tz'),
                            'image_1920': employee_data.get('image_1920'),
                            'active': employee_data.get('active', True),
                            'gender': employee_data.get('gender'),
                            'birthday': employee_data.get('birthday'),
                            'marital': employee_data.get('marital'),
                            'children': employee_data.get('children'),
                            'emergency_contact': employee_data.get('emergency_contact'),
                        }

                        # Add additional fields if they exist in the employee_data dictionary
                        additional_fields = [
                            'address_home_id', 'address_work_id', 'private_email', 'mobile_phone', 'phone', 'fax',
                            'user_id', 'department_id', 'coach_id', 'job_id', 'work_location', 'work_address_id',
                            'work_phone_extension', 'certificate', 'km_home_work', 'expense_limit',
                            'remaining_leaves',
                            'remaining_leaves_hours', 'leave_approver_id', 'resource_calendar_id',
                            'attendance_state',
                            'last_attendance_id', 'last_check_in', 'last_check_out', 'timesheet_cost',
                            'timesheet_ids',
                            'timesheet_not_paid', 'work_email_valid',
                            # Add more fields as needed
                        ]

                        # employee_data.write({'last_sending_date': datetime.now(),})


                        # for field in additional_fields:
                        #     if field in employee_data:
                        #         record_data[field] = employee_data[field]

                        if existing_record:
                            # Update the existing record with the new data
                            existing_record.write(record_data)
                        else:
                            # Create a new record
                            self.create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")
class HRBankInherit(models.Model):
    _inherit = 'res.bank'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def fetch_res_bank_from_api(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + BNK_API_ENDPOINT


            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()


            if response:
                try:
                    employees_list = response_data["data"]["bank"]

                    for employee_data in employees_list:
                        source_id = employee_data.get('id')

                        # Check if a record with the same source_id already exists
                        existing_record = self.search([('source_id', '=', source_id)], limit=1)

                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': employee_data.get('id'),
                            'name': employee_data.get('name'),

                        }

                        if existing_record:
                            # Update the existing record with the new data
                            existing_record.write(record_data)
                        else:
                            # Create a new record
                            self.create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")


class RESPartnerBankInherit(models.Model):
    _inherit = 'res.partner.bank'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def fetch_res_bank_from_api(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + BNK_ACC_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()


            if response:
                try:
                    employees_list = response_data["data"]["bank_account"]

                    for employee_data in employees_list:
                        source_id = employee_data.get('id')
                        partner_id = employee_data.get('partner_id')
                        bank = self.env['res.bank'].search([('source_id', '=', employee_data.get('bank_id'))])
                        partner = self.env['res.partner'].search([('id', '=', partner_id)])

                        if not partner:
                            partner_data = {
                                'name': 'New Partner Name',  # Replace with the actual name
                                # Include other fields as needed
                            }
                            partner = self.env['res.partner'].create(partner_data)

                        # Check if a record with the same source_id already exists
                        existing_record = self.search([('source_id', '=', source_id)], limit=1)


                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': employee_data.get('id'),
                            # 'partner_id': employee_data.get('partner_id'),
                            'partner_id': partner.id,
                            'acc_number': employee_data.get('acc_number'),
                            'acc_holder_name': employee_data.get('acc_holder_name'),
                            'bank_id': bank.id,

                        }

                        if existing_record:
                            # Update the existing record with the new data
                            existing_record.write(record_data)
                        else:
                            # Create a new record
                            self.create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")

class AccountInherit(models.Model):
    _inherit = 'account.analytic.account'

    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)

    def fetch_res_bank_from_api(self):
        session_id = get_session_id()

        if session_id:
            url = BASE_URL + BNK_ACC_ANA_API_ENDPOINT

            payload = json.dumps({
                "jsonrpc": "2.0",
                "params": {}
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'session_id={session_id}'
            }

            response = make_api_request(url, payload, headers)
            response_data = response.json()

            if response:
                try:
                    employees_list = response_data["data"]["account_analytic"]

                    for employee_data in employees_list:
                        source_id = employee_data.get('id')

                        # Check if a record with the same source_id already exists
                        existing_record = self.search([('source_id', '=', source_id)], limit=1)

                        # Prepare the dictionary for creating/updating the record
                        record_data = {
                            'source_id': employee_data.get('id'),
                            # 'last_sending_date': datetime.now(),
                            'name': employee_data.get('name'),

                        }

                        if existing_record:
                            # Update the existing record with the new data
                            existing_record.write(record_data)
                        else:
                            # Create a new record
                            self.create(record_data)

                except json.JSONDecodeError:
                    print("Error: API response is not in valid JSON format.")

class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    # New field for Last Source ID
    source_id = fields.Integer(string="Source ID", help="ID from the external API", readonly=True)
    # New field for Last Sync Date
    last_sync_date = fields.Datetime(string='Last Sync Date', readonly=True)