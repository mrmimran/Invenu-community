from datetime import datetime
import xmlrpc.client
from odoo import models, fields, api
import logging

class SyncModule(models.Model):
    _name = 'sync.module'

    def log_integration_start(self):
        # Add a record to ir.logging for integration start
        self.env['ir.logging'].create({
            'name': 'Integration Start',
            'type': 'server',
            'path': 'path_to_your_server_script',  # Adjust this to the actual path
            'line': 42,  # Adjust this to the actual line number
            'func': 'Integration Start Query : Enterprise - Community',
            'message': f"Integration started at {datetime.now()}"
        })

    def log_integration_end(self):
        # Add a record to ir.logging for integration end
        self.env['ir.logging'].create({
             'name': 'Integration Start',
            'type': 'server',
            'path': 'path_to_your_server_script',  # Adjust this to the actual path
            'line': 42,  # Adjust this to the actual line number
            'func': 'Integration End Query : Enterprise - Community',
            'message': f"Integration started at {datetime.now()}"
        })

    def run_synchronization_enterprise_community(self):
        # Start integration logging
        self.log_integration_start()

        # Prepare XML-RPC client for the enterprise database
        enterprise_url = self.env.company.sync_url
        enterprise_db_name = self.env.company.sync_db
        enterprise_api_login = self.env.company.sync_login
        enterprise_api_pass = self.env.company.sync_pass

        try:
            # Prepare XML-RPC client for enterprise authentication
            enterprise_api = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(enterprise_url))
            logging.info(f"Successfully prepared XML-RPC client for enterprise authentication: {str(enterprise_api)}")
        except Exception as e:
            logging.info(f"Error preparing XML-RPC client for enterprise authentication: {e}")
            return None

        try:
            # Authenticate with the enterprise database and get user ID (uid)
            enterprise_uid = enterprise_api.authenticate(enterprise_db_name, enterprise_api_login, enterprise_api_pass,{})
            logging.info(f"Successfully authenticated enterprise authentication: {str(enterprise_uid)}")
        except Exception as e:
            logging.info(f"Error in authentication with enterprise authentication: {e}")
            return None

        try:
            # Prepare XML-RPC client for interacting with enterprise models
            enterprise_models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(enterprise_url))
            logging.info(f"Successfully prepared XML-RPC client for interacting with enterprise models: {str(enterprise_uid)}")
        except Exception as e:
            logging.info(f"Error in preparing XML-RPC client for interacting with enterprise models: {e}")
            return None

        logging.info (enterprise_api)
        logging.info (enterprise_uid)
        logging.info (enterprise_models)



        # Preparing default fields between both versions
        # resource_calendars_fields = ['name']
        # departments_fields = ['name', 'parent_id', 'manager_id']
        # jobs_fields = ['name', 'department_id']

        # analytic_accounts_fields = ['name']
        # projects_fields = ['name', 'analytic_account_id', 'allow_timesheets', 'employee_project_manager']
        project_fields = ['id','name','label_tasks','partner_id','stage_id','type_ids','date_start','date','allocated_hours','privacy_visibility','alias_name','allow_milestones','is_favorite','is_project_overtime','allow_timesheets','is_milestone_exceeded','allow_task_dependencies','active','alias_incoming_local','is_internal_project','encode_uom_in_days','rating_active','access_token','access_url','alias_email','activity_type_icon','activity_summary','activity_exception_icon','privacy_visibility_warning','label_tasks','display_name','alias_full_name','alias_domain','activity_date_deadline','my_activity_date_deadline','rating_request_deadline','remaining_hours','rating_avg','rating_avg_percentage','description','alias_bounced_content','task_count','closed_task_count','last_update_color','color','total_timesheet_time','collaborator_count','doc_count','rating_count','sequence','rating_percentage_satisfaction','alias_status','rating_status_period','activity_state','privacy_visibility','alias_contact','rating_status','access_warning','alias_defaults','allow_rating']

        project_stage_fields = ['id','active','fold','display_name','name','sequence']

        partner_fields = ['id','name','display_name','parent_id','company_type','country_code','active','company_name','type','street','street2','city','zip','phone','mobile','email','vat']

        task_fields = ['id','name','project_id','effective_hours','progress','stage_id','personal_stage_type_id','personal_stage_type_ids','milestone_id','partner_id','allocated_hours','date_deadline','parent_id','sequence','email_cc','date_assign','date_last_stage_update','working_hours_open','working_days_open','active','allow_timesheets','analytic_account_active','recurring_task','display_parent_task_button','allow_task_dependencies','has_late_and_unreached_milestone','allow_milestones','is_timeoff_task','rating_active','display_in_project','encode_uom_in_days','activity_type_icon','activity_exception_icon','access_url','access_token','portal_user_names','display_name','activity_summary','my_activity_date_deadline','repeat_until','activity_date_deadline','date_end','rating_last_value','rating_avg','rating_percentage_satisfaction','subtask_allocated_hours','working_hours_close','working_days_close','remaining_hours','remaining_hours_percentage','total_hours_spent','overtime','subtask_effective_hours','description','dependent_tasks_count','leave_types_count','repeat_interval','rating_count','recurring_count','subtask_count','closed_subtask_count','color','duration_tracking','repeat_unit','activity_exception_decoration','rating_avg_text','priority','rating_last_text','activity_state','project_privacy_visibility','state','repeat_type','access_warning','rating_last_feedback']

        timesheet_fields = ['id','date','project_id','task_id','name','unit_amount','readonly_timesheet','display_name','job_title','amount','category','employee_id','parent_task_id','manager_id','holiday_id','partner_id']

        employee_fields = ['id','name','active','has_timesheet','is_subordinate','is_absent','show_leaves','work_permit_scheduled_activity','show_hr_icon_display','member_of_department','activity_type_icon','activity_summary','activity_exception_icon','job_title','work_phone','mobile_phone','work_email','last_activity_time','company_country_code','private_street','private_street2','private_city','private_zip','private_phone','private_email','spouse_complete_name','place_of_birth','ssnid','sinid','identification_id','passport_id','permit_no','visa_no','work_permit_name','study_field','study_school','emergency_contact','emergency_phone','barcode','pin','private_car_plate','display_name','allocation_display','allocation_remaining_display','leave_date_from','activity_date_deadline','my_activity_date_deadline','departure_date','leave_date_to','visa_expire','work_permit_expiration_date','spouse_birthdate','last_activity','birthday','leaves_count','remaining_leaves','allocation_count','departure_description','department_color','child_count','km_home_work','children','allocations_count','color','child_all_count','current_leave_id','department_id','job_id','parent_id','coach_id','user_partner_id','activity_state','lang','marital','hr_presence_state','certificate','employee_type','hr_icon_display','current_leave_state','tz','gender','additional_note','notes']

        contract_fields = ['id','active','calendar_mismatch','activity_summary','visa_no','activity_exception_icon','country_code','permit_no','display_name','name','activity_type_icon','first_contract_date','date_end','activity_date_deadline','trial_date_end','my_activity_date_deadline','date_start','notes','contracts_count','job_id','structure_type_id','employee_id','department_id','contract_wage','wage','activity_exception_decoration','kanban_state','state','activity_state']

        attendance_fields = ['id','out_country_name','in_browser','in_ip_address','in_country_name','in_city','display_name','out_browser','out_ip_address','out_city','check_in','check_out','out_latitude','in_latitude','in_longitude','overtime_hours','worked_hours','out_longitude','color','employee_id','department_id','in_mode','out_mode']

        leave_fields = ['id','tz_mismatch','overtime_deductible','has_mandatory_day','is_striked','is_hatched','request_unit_hours','request_unit_half','leave_type_support_document','active','can_cancel','can_approve','can_reset','multi_employee','is_user_only_responsible','active_employee','leave_type_increases_duration','name','activity_type_icon','activity_summary','activity_exception_icon','display_name','private_name','duration_display','number_of_hours_text','request_date_from','activity_date_deadline','my_activity_date_deadline','request_date_to','date_to','date_from','number_of_days','number_of_hours','number_of_days_display','number_of_hours_display','employee_overtime','color','first_approver_id','second_approver_id','department_id','employee_id','holiday_status_id','parent_id','manager_id','category_id','leave_type_request_unit','request_hour_from','request_date_from_period','holiday_type','activity_state','validation_type','activity_exception_decoration','tz','state','request_hour_to','report_note','notes']

        leave_type_fields = ['id','active','has_valid_allocation','hr_attendance_overtime','overtime_deductible','support_document','timesheet_generate','unpaid','display_name','name','accrual_count','group_days_leave','leaves_taken','max_leaves','virtual_remaining_leaves','allocation_count','color','max_allowed_negative','sequence','allocation_validation_type','employee_requests','leave_validation_type','request_unit','requires_allocation','time_type']

        task_type_fields = ['id','fold','active','auto_validation_state','name','display_name','sequence','disabled_rating_warning','description']

        # Preparing Lists: Here we are getting the records that created or changed, here we read all data that we need to create or update
        # resource_calendars = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                                'resource.calendar', 'search_read',
        #                                                [[('sync', '=', True), ('sent', '=', False)]],
        #                                                {'fields': resource_calendars_fields})



        # departments = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                         'hr.department', 'search_read',
        #                                         [[('sync', '=', True), ('sent', '=', False)]],
        #                                         {'fields': departments_fields})
        #
        #
        # jobs = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                  'hr.job', 'search_read',
        #                                  [[('sync', '=', True), ('sent', '=', False)]],
        #                                  {'fields': jobs_fields})

        # employees = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                       'hr.employee', 'search_read',
        #                                       [[('sync', '=', True), ('sent', '=', False)]],
        #                                       {'fields': employees_fields})
        #                                       # {'fields': employees_fields})

        # analytic_accounts = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                               'account.analytic.account', 'search_read',
        #                                               [[('sync', '=', True), ('sent', '=', False)]],
        #                                               {'fields': analytic_accounts_fields})

        # partners = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                      'res.partner', 'search_read',
        #                                      [[('sync', '=', True), ('sent', '=', False)]],
        #                                      {'fields': partner_fields})

        try:
            projects = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'project.project', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': project_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'project.project'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [project.project]: {e}")
            return None
        try:
            tasks = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'project.task', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': task_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'project.task'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [project.task]: {e}")
            return None
        # try:
        #     timesheets = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
        #                                          'account.analytic.line', 'search_read',
        #                                         [[('sync', '=', True), ('sent', '=', False)]],
        #                                          {'fields': timesheet_fields})
        #     logging.info(
        #         f"Successfully read the data from enterprise models: {'account.analytic.line'}")
        # except Exception as e:
        #     logging.info(f"Error in reading data on enterprise models [account.analytic.line]: {e}")
        #     return None
        try:
            employees = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'hr.employee', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': employee_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'hr.employee'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [hr.employee]: {e}")
            return None
        try:
            contracts = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'hr.contract', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': contract_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'hr.contract'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [hr.contract]: {e}")
            return None
        try:
            attendances = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'hr.attendance', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': attendance_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'hr.attendance'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [hr.attendance]: {e}")
            return None
        try:
            leaves = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'hr.leave', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': leave_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'hr.leave'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [hr.leave]: {e}")
            return None
        try:
            leave_types = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'hr.leave.type', 'search_read',
                                                [[('sync', '=', True), ('sent', '=', False)]],
                                                 {'fields': leave_type_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'hr.leave.type'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [hr.leave.type]: {e}")
            return None
        try:
            task_types = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'project.task.type', 'search_read',
                                                [[('sync', '=', True)]],
                                                 {'fields': task_type_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'project.task.type'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [project.task.type]: {e}")
            return None
        try:
            project_stages = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                 'project.project.stage', 'search_read',
                                                [[('sync', '=', True)]],
                                                 {'fields': project_stage_fields})
            logging.info(
                f"Successfully read the data from enterprise models: {'project.project.stage'}")
        except Exception as e:
            logging.info(f"Error in reading data on enterprise models [project.project.stage]: {e}")
            return None

        # logging.info(projects)
        # logging.info(tasks)
        # logging.info(task_types)
        # # logging.info(timesheets)
        # logging.info(employees)
        # logging.info(contract_fields)
        # logging.info(attendances)
        # logging.info(leaves)
        # logging.info(leave_types)
        # logging.info(project_stages)


        # Creation Process, in this step we only add the fields that are static or required in the created object
        # for resource_calendar in resource_calendars:
        #     existing_record = self.env['resource.calendar'].search([('source_id', '=', resource_calendar['id'])])
        #
        #     if not existing_record:
        #         self.env['resource.calendar'].create({
        #             'name': resource_calendar['name'],
        #             'source_id': resource_calendar['id'],
        #             'last_sync_date': datetime.now(),
        #         })

        # for department in departments:
        #     existing_record = self.env['hr.department'].search([('source_id', '=', department['id'])])
        #
        #     if not existing_record:
        #         self.env['hr.department'].create({
        #             'name': department['name'],
        #             'source_id': department['id'],
        #             'last_sync_date': datetime.now(),
        #         })




        # for job in jobs:
        #     existing_record = self.env['hr.job'].search([('source_id', '=', job['id'])])
        #
        #     if not existing_record:
        #         self.env['hr.job'].create({
        #             'name': job['name'],
        #             'source_id': job['id'],
        #             'last_sync_date': datetime.now(),
        #         })
        #
        # for employee in employees:
        #     existing_record = self.env['hr.employee'].search([('source_id', '=', employee['id'])])
        #
        #     if not existing_record:
        #         self.env['hr.employee'].create({
        #             'name': employee['name'],
        #             'source_id': employee['id'],
        #             'last_sync_date': datetime.now(),
        #             # Add other fields here
        #             'image_1920': employee['image_1920'],
        #             'active': employee['active'],
        #             'barcode': employee['barcode'],
        #             # 'vehicle': employee['vehicle'],
        #             'emergency_contact': employee['emergency_contact'],
        #             'emergency_phone': employee['emergency_phone'],
        #             'study_field': employee['study_field'],
        #             'identification_id': employee['identification_id'],
        #             'job_title': employee['job_title'],
        #             'passport_id': employee['passport_id'],
        #             'pin': employee['pin'],
        #             'place_of_birth': employee['place_of_birth'],
        #             'study_school': employee['study_school'],
        #             'sinid': employee['sinid'],
        #             'spouse_complete_name': employee['spouse_complete_name'],
        #             'ssnid': employee['ssnid'],
        #             'visa_no': employee['visa_no'],
        #             'work_email': employee['work_email'],
        #             'mobile_phone': employee['mobile_phone'],
        #             'permit_no': employee['permit_no'],
        #             'work_phone': employee['work_phone'],
        #             'color': employee['color'],
        #             'km_home_work': employee['km_home_work'],
        #             'children': employee['children'],
        #             'certificate': employee['certificate'],
        #             'employee_type': employee['employee_type'],
        #             'gender': employee['gender'],
        #             'marital': employee['marital'],
        #             'additional_note': employee['additional_note'],
        #             'notes': employee['notes']
        #         })
        #
        # for analytic_account in analytic_accounts:
        #     existing_record = self.env['account.analytic.account'].search(
        #         [('source_id', '=', analytic_account['id'])])
        #
        #     if not existing_record:
        #         self.env['account.analytic.account'].create({
        #             'name': analytic_account['name'],
        #             'source_id': analytic_account['id'],
        #             'plan_id': self.env.ref('analytic.analytic_plan_projects').id,
        #             'last_sync_date': datetime.now(),
        #         })

        for employee in employees:
            existing_record = self.env['hr.employee'].search([('source_id', '=', employee['id'])])
            user_partner_id = False
            logging.info("<<<<<<<<<<<<<<< Project Partner ID >>>>>>>>>>>>>>>>>>>")
            if employee['user_partner_id']:
                logging.info(employee['user_partner_id'][0])
                partner, new_create = self.get_record('res.partner', employee['user_partner_id'][0], partner_fields, enterprise_models, enterprise_db_name, enterprise_uid, enterprise_api_pass)
                parent_id = False
                if partner['parent_id']:
                    parent_id = self.env['res.partner'].sudo().search([('source_id', '=', partner['parent_id'])])
                if new_create:
                    logging.info("<<<<<<<<<<<<<< Partner Details >>>>>>>>>>>>>>>>>>>>>")
                    logging.info(partner)

                    user_partner_id =  self.env['res.partner'].create({
                        'name': partner['name'],
                        'display_name': partner['display_name'],
                        'company_type': partner['company_type'],
                        'country_code': partner['country_code'],
                        'active': partner['active'],
                        'company_name': partner['company_name'],
                        'type': partner['type'],
                        'street': partner['street'],
                        'street2': partner['street2'],
                        'city': partner['city'],
                        'zip': partner['zip'],
                        'phone': partner['phone'],
                        'mobile': partner['mobile'],
                        'email': partner['email'],
                        'vat': partner['vat'],
                        'parent_id': parent_id.id if parent_id else False,
                        'source_id': partner['id'],
                        'last_sync_date': datetime.now(),
                    })
                else:
                    user_partner_id = partner

            current_leave_id = False
            if employee['current_leave_id']:
                current_leave_rec = self.env['hr.leave.type'].sudo().search([('source_id','=',employee['current_leave_id'][0])])
                if current_leave_rec:
                    current_leave_id = current_leave_rec

            department_id = False
            if employee['department_id']:
                department_rec = self.env['hr.department'].sudo().search([('source_id','=',employee['department_id'][0])])
                if department_rec:
                    department_id = department_rec

            job_id = False
            if employee['job_id']:
                job_rec = self.env['hr.job'].sudo().search([('source_id','=',employee['job_id'][0])])
                if job_rec:
                    job_id = job_rec

            parent_id = False
            if employee['parent_id']:
                parent_rec = self.env['hr.employee'].sudo().search([('source_id','=',employee['parent_id'][0])])
                if parent_rec:
                    parent_id = parent_rec

            coach_id = False
            if employee['coach_id']:
                coach_rec = self.env['hr.employee'].sudo().search([('source_id','=',employee['coach_id'][0])])
                if coach_rec:
                    coach_id = coach_rec

            if not existing_record:
                self.env['hr.employee'].sudo().create({
                    'source_id': employee['id'],
                    'name': employee['name'],
                    'active': employee['active'],
                    'has_timesheet': employee['has_timesheet'],
                    'is_subordinate': employee['is_subordinate'],
                    'is_absent': employee['is_absent'],
                    'show_leaves': employee['show_leaves'],
                    'work_permit_scheduled_activity': employee['work_permit_scheduled_activity'],
                    # 'newly_hired': employee['newly_hired'],
                    'show_hr_icon_display': employee['show_hr_icon_display'],
                    'member_of_department': employee['member_of_department'],
                    'activity_type_icon': employee['activity_type_icon'],
                    'activity_summary': employee['activity_summary'],
                    'activity_exception_icon': employee['activity_exception_icon'],
                    'job_title': employee['job_title'],
                    'work_phone': employee['work_phone'],
                    'mobile_phone': employee['mobile_phone'],
                    'work_email': employee['work_email'],
                    'last_activity_time': employee['last_activity_time'],
                    'company_country_code': employee['company_country_code'],
                    'private_street': employee['private_street'],
                    'private_street2': employee['private_street2'],
                    'private_city': employee['private_city'],
                    'private_zip': employee['private_zip'],
                    'private_phone': employee['private_phone'],
                    'private_email': employee['private_email'],
                    'spouse_complete_name': employee['spouse_complete_name'],
                    'place_of_birth': employee['place_of_birth'],
                    'ssnid': employee['ssnid'],
                    'sinid': employee['sinid'],
                    'identification_id': employee['identification_id'],
                    'passport_id': employee['passport_id'],
                    'permit_no': employee['permit_no'],
                    'visa_no': employee['visa_no'],
                    'work_permit_name': employee['work_permit_name'],
                    'study_field': employee['study_field'],
                    'study_school': employee['study_school'],
                    'emergency_contact': employee['emergency_contact'],
                    'emergency_phone': employee['emergency_phone'],
                    'barcode': employee['barcode'],
                    'pin': employee['pin'],
                    'private_car_plate': employee['private_car_plate'],
                    'display_name': employee['display_name'],
                    'allocation_display': employee['allocation_display'],
                    'allocation_remaining_display': employee['allocation_remaining_display'],
                    'leave_date_from': employee['leave_date_from'],
                    'activity_date_deadline': employee['activity_date_deadline'],
                    'my_activity_date_deadline': employee['my_activity_date_deadline'],
                    'departure_date': employee['departure_date'],
                    'leave_date_to': employee['leave_date_to'],
                    'visa_expire': employee['visa_expire'],
                    'work_permit_expiration_date': employee['work_permit_expiration_date'],
                    'spouse_birthdate': employee['spouse_birthdate'],
                    'last_activity': employee['last_activity'],
                    'birthday': employee['birthday'],
                    'leaves_count': employee['leaves_count'],
                    'remaining_leaves': employee['remaining_leaves'],
                    'allocation_count': employee['allocation_count'],
                    'departure_description': employee['departure_description'],
                    'department_color': employee['department_color'],
                    'child_count': employee['child_count'],
                    'km_home_work': employee['km_home_work'],
                    'children': employee['children'],
                    'allocations_count': employee['allocations_count'],
                    'color': employee['color'],
                    'child_all_count': employee['child_all_count'],
                    'current_leave_id': current_leave_id.id if current_leave_id else False,
                    'department_id': department_id.id if department_id else False,
                    'job_id': job_id.id if job_id else False,
                    'parent_id': parent_id.id if parent_id else False,
                    'coach_id': coach_id.id if coach_id else False,
                    'user_partner_id': user_partner_id.id if user_partner_id else False,
                    'activity_state': employee['activity_state'],
                    'lang': employee['lang'],
                    'marital': employee['marital'],
                    'hr_presence_state': employee['hr_presence_state'],
                    'certificate': employee['certificate'],
                    'employee_type': employee['employee_type'],
                    'hr_icon_display': employee['hr_icon_display'],
                    'current_leave_state': employee['current_leave_state'],
                    'tz': employee['tz'],
                    'gender': employee['gender'],
                    'additional_note': employee['additional_note'],
                    'notes': employee['notes'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'source_id': employee['id'],
                    'name': employee['name'],
                    'active': employee['active'],
                    'has_timesheet': employee['has_timesheet'],
                    'is_subordinate': employee['is_subordinate'],
                    'is_absent': employee['is_absent'],
                    'show_leaves': employee['show_leaves'],
                    'work_permit_scheduled_activity': employee['work_permit_scheduled_activity'],
                    # 'newly_hired': employee['newly_hired'],
                    'show_hr_icon_display': employee['show_hr_icon_display'],
                    'member_of_department': employee['member_of_department'],
                    'activity_type_icon': employee['activity_type_icon'],
                    'activity_summary': employee['activity_summary'],
                    'activity_exception_icon': employee['activity_exception_icon'],
                    'job_title': employee['job_title'],
                    'work_phone': employee['work_phone'],
                    'mobile_phone': employee['mobile_phone'],
                    'work_email': employee['work_email'],
                    'last_activity_time': employee['last_activity_time'],
                    'company_country_code': employee['company_country_code'],
                    'private_street': employee['private_street'],
                    'private_street2': employee['private_street2'],
                    'private_city': employee['private_city'],
                    'private_zip': employee['private_zip'],
                    'private_phone': employee['private_phone'],
                    'private_email': employee['private_email'],
                    'spouse_complete_name': employee['spouse_complete_name'],
                    'place_of_birth': employee['place_of_birth'],
                    'ssnid': employee['ssnid'],
                    'sinid': employee['sinid'],
                    'identification_id': employee['identification_id'],
                    'passport_id': employee['passport_id'],
                    'permit_no': employee['permit_no'],
                    'visa_no': employee['visa_no'],
                    'work_permit_name': employee['work_permit_name'],
                    'study_field': employee['study_field'],
                    'study_school': employee['study_school'],
                    'emergency_contact': employee['emergency_contact'],
                    'emergency_phone': employee['emergency_phone'],
                    'barcode': employee['barcode'],
                    'pin': employee['pin'],
                    'private_car_plate': employee['private_car_plate'],
                    'display_name': employee['display_name'],
                    'allocation_display': employee['allocation_display'],
                    'allocation_remaining_display': employee['allocation_remaining_display'],
                    'leave_date_from': employee['leave_date_from'],
                    'activity_date_deadline': employee['activity_date_deadline'],
                    'my_activity_date_deadline': employee['my_activity_date_deadline'],
                    'departure_date': employee['departure_date'],
                    'leave_date_to': employee['leave_date_to'],
                    'visa_expire': employee['visa_expire'],
                    'work_permit_expiration_date': employee['work_permit_expiration_date'],
                    'spouse_birthdate': employee['spouse_birthdate'],
                    'last_activity': employee['last_activity'],
                    'birthday': employee['birthday'],
                    'leaves_count': employee['leaves_count'],
                    'remaining_leaves': employee['remaining_leaves'],
                    'allocation_count': employee['allocation_count'],
                    'departure_description': employee['departure_description'],
                    'department_color': employee['department_color'],
                    'child_count': employee['child_count'],
                    'km_home_work': employee['km_home_work'],
                    'children': employee['children'],
                    'allocations_count': employee['allocations_count'],
                    'color': employee['color'],
                    'child_all_count': employee['child_all_count'],
                    'current_leave_id': current_leave_id.id if current_leave_id else False,
                    'department_id': department_id.id if department_id else False,
                    'job_id': job_id.id if job_id else False,
                    'parent_id': parent_id.id if parent_id else False,
                    'coach_id': coach_id.id if coach_id else False,
                    'user_partner_id': user_partner_id.id if user_partner_id else False,
                    'activity_state': employee['activity_state'],
                    'lang': employee['lang'],
                    'marital': employee['marital'],
                    'hr_presence_state': employee['hr_presence_state'],
                    'certificate': employee['certificate'],
                    'employee_type': employee['employee_type'],
                    'hr_icon_display': employee['hr_icon_display'],
                    'current_leave_state': employee['current_leave_state'],
                    'tz': employee['tz'],
                    'gender': employee['gender'],
                    'additional_note': employee['additional_note'],
                    'notes': employee['notes'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for contract in contracts:
            existing_record = self.env['hr.contract'].search([('source_id', '=', contract['id'])])

            employee_id = False
            if contract['employee_id']:
                employee_rec = self.env['hr.employee'].sudo().search([('source_id','=',contract['employee_id'][0])])
                if employee_rec:
                    employee_id = employee_rec

            job_id = False
            if contract['job_id']:
                job_rec = self.env['hr.job'].sudo().search([('source_id','=',contract['job_id'][0])])
                if job_rec:
                    job_id = job_rec

            department_id = False
            if contract['department_id']:
                department_rec = self.env['hr.department'].sudo().search([('source_id','=',contract['department_id'][0])])
                if department_rec:
                    department_id = department_rec

            structure_type_id = False
            if contract['structure_type_id']:
                structure_type_rec = self.env['hr.payroll.structure.type'].sudo().search([('source_id','=',contract['structure_type_id'][0])])
                if structure_type_rec:
                    structure_type_id = structure_type_rec

            if not existing_record:
                self.env['hr.contract'].sudo().create({
                    'source_id': contract['id'],
                    'active': contract['active'],
                    # 'sent': contract['sent'],
                    'calendar_mismatch': contract['calendar_mismatch'],
                    'activity_summary': contract['activity_summary'],
                    'visa_no': contract['visa_no'],
                    'activity_exception_icon': contract['activity_exception_icon'],
                    'country_code': contract['country_code'],
                    'permit_no': contract['permit_no'],
                    'display_name': contract['display_name'],
                    'name': contract['name'],
                    'activity_type_icon': contract['activity_type_icon'],
                    'first_contract_date': contract['first_contract_date'],
                    'date_end': contract['date_end'],
                    'activity_date_deadline': contract['activity_date_deadline'],
                    'trial_date_end': contract['trial_date_end'],
                    'my_activity_date_deadline': contract['my_activity_date_deadline'],
                    'date_start': contract['date_start'],
                    'notes': contract['notes'],
                    'contracts_count': contract['contracts_count'],
                    'job_id': job_id.id if job_id else False,
                    'structure_type_id': structure_type_id.id if structure_type_id else False,
                    'employee_id': employee_id.id if employee_id else False,
                    'department_id': department_id.id if department_id else False,
                    'contract_wage': contract['contract_wage'],
                    'wage': contract['wage'],
                    'activity_exception_decoration': contract['activity_exception_decoration'],
                    'kanban_state': contract['kanban_state'],
                    'state': contract['state'],
                    'activity_state': contract['activity_state'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'source_id': contract['id'],
                    'active': contract['active'],
                    # 'sent': contract['sent'],
                    'calendar_mismatch': contract['calendar_mismatch'],
                    'activity_summary': contract['activity_summary'],
                    'visa_no': contract['visa_no'],
                    'activity_exception_icon': contract['activity_exception_icon'],
                    'country_code': contract['country_code'],
                    'permit_no': contract['permit_no'],
                    'display_name': contract['display_name'],
                    'name': contract['name'],
                    'activity_type_icon': contract['activity_type_icon'],
                    'first_contract_date': contract['first_contract_date'],
                    'date_end': contract['date_end'],
                    'activity_date_deadline': contract['activity_date_deadline'],
                    'trial_date_end': contract['trial_date_end'],
                    'my_activity_date_deadline': contract['my_activity_date_deadline'],
                    'date_start': contract['date_start'],
                    'notes': contract['notes'],
                    'contracts_count': contract['contracts_count'],
                    'job_id': job_id.id if job_id else False,
                    'structure_type_id': structure_type_id.id if structure_type_id else False,
                    'employee_id': employee_id.id if employee_id else False,
                    'department_id': department_id.id if department_id else False,
                    'contract_wage': contract['contract_wage'],
                    'wage': contract['wage'],
                    'activity_exception_decoration': contract['activity_exception_decoration'],
                    'kanban_state': contract['kanban_state'],
                    'state': contract['state'],
                    'activity_state': contract['activity_state'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for task_type in task_types:
            existing_record = self.env['project.task.type'].search([('source_id', '=', task_type['id'])])


            if not existing_record:
                self.env['project.task.type'].sudo().create({
                    'source_id': task_type['id'],
                    'fold': task_type['fold'],
                    'user_id': False,
                    'active': task_type['active'],
                    'auto_validation_state': task_type['auto_validation_state'],
                    'name': task_type['name'],
                    'display_name': task_type['display_name'],
                    'sequence': task_type['sequence'],
                    'disabled_rating_warning': task_type['disabled_rating_warning'],
                    'description': task_type['description'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'fold': task_type['fold'],
                    'active': task_type['active'],
                    'user_id': False,
                    'auto_validation_state': task_type['auto_validation_state'],
                    'name': task_type['name'],
                    'display_name': task_type['display_name'],
                    'sequence': task_type['sequence'],
                    'disabled_rating_warning': task_type['disabled_rating_warning'],
                    'description': task_type['description'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for project_stage in project_stages:
            existing_record = self.env['project.project.stage'].search([('source_id', '=', project_stage['id'])])

            ['id', 'active', 'fold', 'display_name', 'name', 'sequence']
            if not existing_record:
                self.env['project.project.stage'].sudo().create({
                    'source_id': project_stage['id'],
                    'active': project_stage['active'],
                    'fold': project_stage['fold'],
                    'display_name': project_stage['display_name'],
                    'name': project_stage['name'],
                    'sequence': project_stage['sequence'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'active': project_stage['active'],
                    'fold': project_stage['fold'],
                    'display_name': project_stage['display_name'],
                    'name': project_stage['name'],
                    'sequence': project_stage['sequence'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for project in projects:
            existing_record = self.env['project.project'].search([('source_id', '=', project['id'])])

            logging.info("<<<<<<<<<<< Project Type Ids >>>>>>>>>>>>>>>>>>>")
            logging.info(project['type_ids'])

            partner_id = False
            logging.info("<<<<<<<<<<<<<<< Project Partner ID >>>>>>>>>>>>>>>>>>>")
            if project['partner_id']:
                logging.info(project['partner_id'][0])
                partner, new_create = self.get_record('res.partner', project['partner_id'][0], partner_fields, enterprise_models, enterprise_db_name, enterprise_uid, enterprise_api_pass)
                parent_id = False
                if partner['parent_id']:
                    parent_id = self.env['res.partner'].sudo().search([('source_id', '=', partner['parent_id'])])
                if new_create:
                    logging.info("<<<<<<<<<<<<<< Partner Details >>>>>>>>>>>>>>>>>>>>>")
                    logging.info(partner)

                    partner_id =  self.env['res.partner'].create({
                        'name': partner['name'],
                        'display_name': partner['display_name'],
                        'company_type': partner['company_type'],
                        'country_code': partner['country_code'],
                        'active': partner['active'],
                        'company_name': partner['company_name'],
                        'type': partner['type'],
                        'street': partner['street'],
                        'street2': partner['street2'],
                        'city': partner['city'],
                        'zip': partner['zip'],
                        'phone': partner['phone'],
                        'mobile': partner['mobile'],
                        'email': partner['email'],
                        'vat': partner['vat'],
                        'parent_id': parent_id.id if parent_id else False,
                        'source_id': partner['id'],
                        'last_sync_date': datetime.now(),
                    })
                else:
                    partner_id = partner

            type_ids = False
            if project['type_ids']:
                task_type_recs = self.env['project.task.type'].sudo().search(
                    [('source_id', 'in', project['type_ids'])]).ids
                if task_type_recs:
                    type_ids = task_type_recs

            stage_id = False
            logging.info("<<<<<<<<<<<<<<<< Project Stage >>>>>>>>>>>>>>>>>>")
            logging.info(project['stage_id'][0])
            if project['stage_id']:
                stage_rec = self.env['project.project.stage'].sudo().search(
                    [('source_id', '=', project['stage_id'][0])])
                if stage_rec:
                    stage_id = stage_rec

            if not existing_record:
                self.env['project.project'].sudo().create({
                    'source_id': project['id'],
                    'name': project['name'],
                    'label_tasks': project['label_tasks'],
                    'partner_id': partner_id.id if partner_id else False,
                    'stage_id': stage_id.id if stage_id else False,
                    'type_ids': [(6, 0, type_ids)] if type_ids else False,
                    # 'parent_id': parent_id.id if parent_id else False,
                    'date_start': project['date_start'],
                    'date': project['date'],
                    'allocated_hours': project['allocated_hours'],
                    'privacy_visibility': project['privacy_visibility'],
                    'alias_name': project['alias_name'],
                    'allow_milestones': project['allow_milestones'],
                    'allow_timesheets': project['allow_timesheets'],
                    'is_favorite': project['is_favorite'],
                    'is_project_overtime': project['is_project_overtime'],
                    'allow_timesheets': project['allow_timesheets'],
                    'is_milestone_exceeded': project['is_milestone_exceeded'],
                    'allow_task_dependencies': project['allow_task_dependencies'],
                    'active': project['active'],
                    'alias_incoming_local': project['alias_incoming_local'],
                    'is_internal_project': project['is_internal_project'],
                    'encode_uom_in_days': project['encode_uom_in_days'],
                    'rating_active': project['rating_active'],
                    'access_token': project['access_token'],
                    'access_url': project['access_url'],
                    'alias_email': project['alias_email'],
                    'activity_type_icon': project['activity_type_icon'],
                    'activity_summary': project['activity_summary'],
                    'activity_exception_icon': project['activity_exception_icon'],
                    'privacy_visibility_warning': project['privacy_visibility_warning'],
                    'label_tasks': project['label_tasks'],
                    'display_name': project['display_name'],
                    'alias_full_name': project['alias_full_name'],
                    'alias_domain': project['alias_domain'],
                    'activity_date_deadline': project['activity_date_deadline'],
                    'my_activity_date_deadline': project['my_activity_date_deadline'],
                    'rating_request_deadline': project['rating_request_deadline'],
                    'remaining_hours': project['remaining_hours'],
                    'rating_avg': project['rating_avg'],
                    'rating_avg_percentage': project['rating_avg_percentage'],
                    'description': project['description'],
                    'alias_bounced_content': project['alias_bounced_content'],
                    'task_count': project['task_count'],
                    'closed_task_count': project['closed_task_count'],
                    'last_update_color': project['last_update_color'],
                    'color': project['color'],
                    'total_timesheet_time': project['total_timesheet_time'],
                    'collaborator_count': project['collaborator_count'],
                    'doc_count': project['doc_count'],
                    'rating_count': project['rating_count'],
                    'sequence': project['sequence'],
                    'rating_percentage_satisfaction': project['rating_percentage_satisfaction'],
                    'alias_status': project['alias_status'],
                    'rating_status_period': project['rating_status_period'],
                    'activity_state': project['activity_state'],
                    'privacy_visibility': project['privacy_visibility'],
                    'alias_contact': project['alias_contact'],
                    'rating_status': project['rating_status'],
                    'access_warning': project['access_warning'],
                    'alias_defaults': project['alias_defaults'],
                    'allow_rating': project['allow_rating'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'name': project['name'],
                    'label_tasks': project['label_tasks'],
                    'partner_id': partner_id.id if partner_id else False,
                    'stage_id': stage_id.id if stage_id else False,
                    'date_start': project['date_start'],
                    'date': project['date'],
                    'type_ids': [(6, 0, type_ids)] if type_ids else False,
                    'allocated_hours': project['allocated_hours'],
                    'privacy_visibility': project['privacy_visibility'],
                    'alias_name': project['alias_name'],
                    'allow_milestones': project['allow_milestones'],
                    'allow_timesheets': project['allow_timesheets'],
                    'is_favorite': project['is_favorite'],
                    'is_project_overtime': project['is_project_overtime'],
                    'allow_timesheets': project['allow_timesheets'],
                    'is_milestone_exceeded': project['is_milestone_exceeded'],
                    'allow_task_dependencies': project['allow_task_dependencies'],
                    'active': project['active'],
                    'alias_incoming_local': project['alias_incoming_local'],
                    'is_internal_project': project['is_internal_project'],
                    'encode_uom_in_days': project['encode_uom_in_days'],
                    'rating_active': project['rating_active'],
                    'access_token': project['access_token'],
                    'access_url': project['access_url'],
                    'alias_email': project['alias_email'],
                    'activity_type_icon': project['activity_type_icon'],
                    'activity_summary': project['activity_summary'],
                    'activity_exception_icon': project['activity_exception_icon'],
                    'privacy_visibility_warning': project['privacy_visibility_warning'],
                    'label_tasks': project['label_tasks'],
                    'display_name': project['display_name'],
                    'alias_full_name': project['alias_full_name'],
                    'alias_domain': project['alias_domain'],
                    'activity_date_deadline': project['activity_date_deadline'],
                    'my_activity_date_deadline': project['my_activity_date_deadline'],
                    'rating_request_deadline': project['rating_request_deadline'],
                    'remaining_hours': project['remaining_hours'],
                    'rating_avg': project['rating_avg'],
                    'rating_avg_percentage': project['rating_avg_percentage'],
                    'description': project['description'],
                    'alias_bounced_content': project['alias_bounced_content'],
                    'task_count': project['task_count'],
                    'closed_task_count': project['closed_task_count'],
                    'last_update_color': project['last_update_color'],
                    'color': project['color'],
                    'total_timesheet_time': project['total_timesheet_time'],
                    'collaborator_count': project['collaborator_count'],
                    'doc_count': project['doc_count'],
                    'rating_count': project['rating_count'],
                    'sequence': project['sequence'],
                    'rating_percentage_satisfaction': project['rating_percentage_satisfaction'],
                    'alias_status': project['alias_status'],
                    'rating_status_period': project['rating_status_period'],
                    'activity_state': project['activity_state'],
                    'privacy_visibility': project['privacy_visibility'],
                    'alias_contact': project['alias_contact'],
                    'rating_status': project['rating_status'],
                    'access_warning': project['access_warning'],
                    'alias_defaults': project['alias_defaults'],
                    'allow_rating': project['allow_rating'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for task in tasks:
            existing_record = self.env['project.task'].search([('source_id', '=', task['id'])])
            partner_id = False
            logging.info("<<<<<<<<<<<<<<< Task Partner ID >>>>>>>>>>>>>>>>>>>")
            if task['partner_id']:
                logging.info(task['partner_id'][0])
                partner, task_partner_new_create = self.get_record('res.partner', task['partner_id'][0], partner_fields, enterprise_models, enterprise_db_name, enterprise_uid, enterprise_api_pass)
                parent_id = False
                if partner['parent_id']:
                    parent_id = self.env['res.partner'].sudo().search([('source_id', '=', partner['parent_id'])])
                if task_partner_new_create:
                    logging.info("<<<<<<<<<<<<<< Partner Details >>>>>>>>>>>>>>>>>>>>>")
                    logging.info(partner)

                    partner_id =  self.env['res.partner'].create({
                        'name': partner['name'],
                        'display_name': partner['display_name'],
                        'company_type': partner['company_type'],
                        'country_code': partner['country_code'],
                        'active': partner['active'],
                        'company_name': partner['company_name'],
                        'type': partner['type'],
                        'street': partner['street'],
                        'street2': partner['street2'],
                        'city': partner['city'],
                        'zip': partner['zip'],
                        'phone': partner['phone'],
                        'mobile': partner['mobile'],
                        'email': partner['email'],
                        'vat': partner['vat'],
                        'parent_id': parent_id.id if parent_id else False,
                        'source_id': partner['id'],
                        'last_sync_date': datetime.now(),
                    })
                else:
                    partner_id = partner

            logging.info("<<<<<<<<<<<<<<< Task Project ID >>>>>>>>>>>>>>>>>>>")
            project_id = False
            if task['project_id']:
                project_rec = self.env['project.project'].sudo().search(
                    [('source_id', '=', task['project_id'][0])])
                if project_rec:
                    project_id = project_rec
            parent_id = False
            if task['parent_id']:
                parent_rec = self.env['project.task'].sudo().search(
                    [('source_id', '=', task['parent_id'][0])])
                if parent_rec:
                    parent_id = parent_rec
            stage_id = False
            if task['stage_id']:
                stage_rec = self.env['project.task.type'].sudo().search(
                    [('source_id', '=', task['stage_id'][0])])
                if stage_rec:
                    stage_id = stage_rec
            personal_stage_type_id = False
            if task['personal_stage_type_id']:
                personal_stage_rec = self.env['project.task.type'].sudo().search(
                    [('source_id', '=', task['personal_stage_type_id'][0])])
                if personal_stage_rec:
                    personal_stage_type_id = personal_stage_rec

            personal_stage_type_ids = False
            if task['personal_stage_type_ids']:
                personal_stage_type_recs = self.env['project.task.type'].sudo().search(
                    [('source_id', 'in', task['personal_stage_type_ids'][0])]).ids
                if personal_stage_type_recs:
                    personal_stage_type_ids = personal_stage_type_recs
                    personal_stage_type_ids

            if not existing_record:
                self.env['project.task'].sudo().create({
                    'source_id': task['id'],
                    'name': task['name'],
                    'project_id': project_id.id if project_id else False,
                    'personal_stage_type_ids': [(6, 0, personal_stage_type_ids)] if personal_stage_type_ids else False,
                    'effective_hours': task['effective_hours'],
                    'progress': task['progress'],
                    'stage_id': stage_id.id if stage_id else False,
                    'personal_stage_type_id': personal_stage_type_id.id if personal_stage_type_id else False,
                    # 'milestone_id': task['milestone_id'],
                    'partner_id': partner_id.id if partner_id else False,
                    'allocated_hours': task['allocated_hours'],
                    'date_deadline': task['date_deadline'],
                    'parent_id': parent_id.id if parent_id else False,
                    'sequence': task['sequence'],
                    'email_cc': task['email_cc'],
                    'date_assign': task['date_assign'],
                    'date_last_stage_update': task['date_last_stage_update'],
                    'working_hours_open': task['working_hours_open'],
                    'working_days_open': task['working_days_open'],
                    'active': task['active'],
                    'allow_timesheets': task['allow_timesheets'],
                    'analytic_account_active': task['analytic_account_active'],
                    'recurring_task': task['recurring_task'],
                    'display_parent_task_button': task['display_parent_task_button'],
                    'allow_task_dependencies': task['allow_task_dependencies'],
                    'has_late_and_unreached_milestone': task['has_late_and_unreached_milestone'],
                    'allow_milestones': task['allow_milestones'],
                    'is_timeoff_task': task['is_timeoff_task'],
                    'rating_active': task['rating_active'],
                    'display_in_project': task['display_in_project'],
                    'encode_uom_in_days': task['encode_uom_in_days'],
                    'activity_type_icon': task['activity_type_icon'],
                    'activity_exception_icon': task['activity_exception_icon'],
                    'access_url': task['access_url'],
                    'access_token': task['access_token'],
                    'portal_user_names': task['portal_user_names'],
                    'display_name': task['display_name'],
                    'activity_summary': task['activity_summary'],
                    'my_activity_date_deadline': task['my_activity_date_deadline'],
                    'repeat_until': task['repeat_until'],
                    'activity_date_deadline': task['activity_date_deadline'],
                    'date_end': task['date_end'],
                    'rating_last_value': task['rating_last_value'],
                    'rating_avg': task['rating_avg'],
                    'rating_percentage_satisfaction': task['rating_percentage_satisfaction'],
                    'subtask_allocated_hours': task['subtask_allocated_hours'],
                    'working_hours_close': task['working_hours_close'],
                    'working_days_close': task['working_days_close'],
                    'remaining_hours': task['remaining_hours'],
                    'remaining_hours_percentage': task['remaining_hours_percentage'],
                    'total_hours_spent': task['total_hours_spent'],
                    'overtime': task['overtime'],
                    'subtask_effective_hours': task['subtask_effective_hours'],
                    'description': task['description'],
                    'dependent_tasks_count': task['dependent_tasks_count'],
                    'leave_types_count': task['leave_types_count'],
                    'repeat_interval': task['repeat_interval'],
                    'rating_count': task['rating_count'],
                    'recurring_count': task['recurring_count'],
                    'subtask_count': task['subtask_count'],
                    'closed_subtask_count': task['closed_subtask_count'],
                    'color': task['color'],
                    'duration_tracking': task['duration_tracking'],
                    'repeat_unit': task['repeat_unit'],
                    'activity_exception_decoration': task['activity_exception_decoration'],
                    'rating_avg_text': task['rating_avg_text'],
                    'priority': task['priority'],
                    'rating_last_text': task['rating_last_text'],
                    'activity_state': task['activity_state'],
                    'project_privacy_visibility': task['project_privacy_visibility'],
                    'state': task['state'],
                    'repeat_type': task['repeat_type'],
                    'access_warning': task['access_warning'],
                    'rating_last_feedback': task['rating_last_feedback'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'name': task['name'],
                    'project_id': project_id.id if project_id else False,
                    'personal_stage_type_ids': [(6, 0, personal_stage_type_ids)] if personal_stage_type_ids else False,
                    'effective_hours': task['effective_hours'],
                    'progress': task['progress'],
                    'stage_id': stage_id.id if stage_id else False,
                    # 'milestone_id': task['milestone_id'],
                    'partner_id': partner_id.id if partner_id else False,
                    'allocated_hours': task['allocated_hours'],
                    'date_deadline': task['date_deadline'],
                    # 'parent_id': task['parent_id'],
                    'sequence': task['sequence'],
                    'email_cc': task['email_cc'],
                    'date_assign': task['date_assign'],
                    'date_last_stage_update': task['date_last_stage_update'],
                    'working_hours_open': task['working_hours_open'],
                    'working_days_open': task['working_days_open'],
                    'active': task['active'],
                    'allow_timesheets': task['allow_timesheets'],
                    'analytic_account_active': task['analytic_account_active'],
                    'recurring_task': task['recurring_task'],
                    'display_parent_task_button': task['display_parent_task_button'],
                    'allow_task_dependencies': task['allow_task_dependencies'],
                    'has_late_and_unreached_milestone': task['has_late_and_unreached_milestone'],
                    'allow_milestones': task['allow_milestones'],
                    'is_timeoff_task': task['is_timeoff_task'],
                    'rating_active': task['rating_active'],
                    'display_in_project': task['display_in_project'],
                    'encode_uom_in_days': task['encode_uom_in_days'],
                    'activity_type_icon': task['activity_type_icon'],
                    'activity_exception_icon': task['activity_exception_icon'],
                    'access_url': task['access_url'],
                    'access_token': task['access_token'],
                    'portal_user_names': task['portal_user_names'],
                    'display_name': task['display_name'],
                    'activity_summary': task['activity_summary'],
                    'my_activity_date_deadline': task['my_activity_date_deadline'],
                    'repeat_until': task['repeat_until'],
                    'activity_date_deadline': task['activity_date_deadline'],
                    'date_end': task['date_end'],
                    'rating_last_value': task['rating_last_value'],
                    'rating_avg': task['rating_avg'],
                    'rating_percentage_satisfaction': task['rating_percentage_satisfaction'],
                    'subtask_allocated_hours': task['subtask_allocated_hours'],
                    'working_hours_close': task['working_hours_close'],
                    'working_days_close': task['working_days_close'],
                    'remaining_hours': task['remaining_hours'],
                    'remaining_hours_percentage': task['remaining_hours_percentage'],
                    'total_hours_spent': task['total_hours_spent'],
                    'overtime': task['overtime'],
                    'subtask_effective_hours': task['subtask_effective_hours'],
                    'description': task['description'],
                    'dependent_tasks_count': task['dependent_tasks_count'],
                    'leave_types_count': task['leave_types_count'],
                    'repeat_interval': task['repeat_interval'],
                    'rating_count': task['rating_count'],
                    'recurring_count': task['recurring_count'],
                    'subtask_count': task['subtask_count'],
                    'closed_subtask_count': task['closed_subtask_count'],
                    'color': task['color'],
                    'duration_tracking': task['duration_tracking'],
                    'repeat_unit': task['repeat_unit'],
                    'activity_exception_decoration': task['activity_exception_decoration'],
                    'rating_avg_text': task['rating_avg_text'],
                    'priority': task['priority'],
                    'rating_last_text': task['rating_last_text'],
                    'activity_state': task['activity_state'],
                    'project_privacy_visibility': task['project_privacy_visibility'],
                    'state': task['state'],
                    'repeat_type': task['repeat_type'],
                    'access_warning': task['access_warning'],
                    'rating_last_feedback': task['rating_last_feedback'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for leave_type in leave_types:
            existing_record = self.env['hr.leave.type'].search([('source_id', '=', leave_type['id'])])
            # employee_id = False
            # if leave_type['employee_id']:
            #     employee_rec = self.env['hr.employee'].sudo().search([('source_id','=',leave_type['employee_id'][0])])
            #     if employee_rec:
            #         employee_id = employee_rec

            if not existing_record:
                self.env['hr.leave.type'].sudo().create({
                    'source_id': leave_type['id'],
                    'active': leave_type['active'],
                    # 'allows_negative_caps': leave_type['allows_negative_caps'],
                    'has_valid_allocation': leave_type['has_valid_allocation'],
                    'hr_attendance_overtime': leave_type['hr_attendance_overtime'],
                    'overtime_deductible': leave_type['overtime_deductible'],
                    'support_document': leave_type['support_document'],
                    'timesheet_generate': leave_type['timesheet_generate'],
                    'unpaid': leave_type['unpaid'],
                    'display_name': leave_type['display_name'],
                    'name': leave_type['name'],
                    'accrual_count': leave_type['accrual_count'],
                    'group_days_leave': leave_type['group_days_leave'],
                    'leaves_taken': leave_type['leaves_taken'],
                    'max_leaves': leave_type['max_leaves'],
                    'virtual_remaining_leaves': leave_type['virtual_remaining_leaves'],
                    'allocation_count': leave_type['allocation_count'],
                    'color': leave_type['color'],
                    'max_allowed_negative': leave_type['max_allowed_negative'],
                    'sequence': leave_type['sequence'],
                    'allocation_validation_type': leave_type['allocation_validation_type'],
                    'employee_requests': leave_type['employee_requests'],
                    'leave_validation_type': leave_type['leave_validation_type'],
                    'request_unit': leave_type['request_unit'],
                    'requires_allocation': leave_type['requires_allocation'],
                    'time_type': leave_type['time_type'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'source_id': leave_type['id'],
                    'active': leave_type['active'],
                    # 'allows_negative_caps': leave_type['allows_negative_caps'],
                    'has_valid_allocation': leave_type['has_valid_allocation'],
                    'hr_attendance_overtime': leave_type['hr_attendance_overtime'],
                    'overtime_deductible': leave_type['overtime_deductible'],
                    'support_document': leave_type['support_document'],
                    'timesheet_generate': leave_type['timesheet_generate'],
                    'unpaid': leave_type['unpaid'],
                    'display_name': leave_type['display_name'],
                    'name': leave_type['name'],
                    'accrual_count': leave_type['accrual_count'],
                    'group_days_leave': leave_type['group_days_leave'],
                    'leaves_taken': leave_type['leaves_taken'],
                    'max_leaves': leave_type['max_leaves'],
                    'virtual_remaining_leaves': leave_type['virtual_remaining_leaves'],
                    'allocation_count': leave_type['allocation_count'],
                    'color': leave_type['color'],
                    'max_allowed_negative': leave_type['max_allowed_negative'],
                    'sequence': leave_type['sequence'],
                    'allocation_validation_type': leave_type['allocation_validation_type'],
                    'employee_requests': leave_type['employee_requests'],
                    'leave_validation_type': leave_type['leave_validation_type'],
                    'request_unit': leave_type['request_unit'],
                    'requires_allocation': leave_type['requires_allocation'],
                    'time_type': leave_type['time_type'],
                    'last_sync_date': fields.Datetime.now(),
                })

        for leave in leaves:
            existing_record = self.env['hr.leave'].search([('source_id', '=', leave['id'])])
            partner_id = False
            logging.info("<<<<<<<<<<<<<<< Project Partner ID >>>>>>>>>>>>>>>>>>>")

            employee_id = False
            if leave['employee_id']:
                employee_rec = self.env['hr.employee'].sudo().search([('source_id','=',leave['employee_id'][0])])
                if employee_rec:
                    employee_id = employee_rec

            first_approver_id = False
            if leave['first_approver_id']:
                first_approver_rec = self.env['hr.employee'].sudo().search([('source_id','=',leave['first_approver_id'][0])])
                if first_approver_rec:
                    first_approver_id = first_approver_rec

            second_approver_id = False
            if leave['second_approver_id']:
                second_approver_rec = self.env['hr.employee'].sudo().search([('source_id','=',leave['second_approver_id'][0])])
                if second_approver_rec:
                    second_approver_id = second_approver_rec

            department_id = False
            if leave['department_id']:
                department_rec = self.env['hr.department'].sudo().search([('source_id','=',leave['department_id'][0])])
                if department_rec:
                    department_id = department_rec

            holiday_status_id = False
            if leave['holiday_status_id']:
                holiday_status_rec = self.env['hr.leave.type'].sudo().search([('source_id','=',leave['holiday_status_id'][0])])
                if holiday_status_rec:
                    holiday_status_id = holiday_status_rec

            parent_id = False
            if leave['parent_id']:
                parent_rec = self.env['hr.leave'].sudo().search([('source_id','=',leave['parent_id'][0])])
                if parent_rec:
                    parent_id = parent_rec

            manager_id = False
            if leave['manager_id']:
                manager_rec = self.env['hr.employee'].sudo().search([('source_id','=',leave['manager_id'][0])])
                if manager_rec:
                    manager_id = manager_rec

            category_id = False
            if leave['category_id']:
                category_rec = self.env['hr.employee.category'].sudo().search([('source_id','=',leave['category_id'][0])])
                if category_rec:
                    category_id = category_rec

            if not existing_record:
                self.env['hr.leave'].sudo().create({
                    'source_id': leave['id'],
                    'tz_mismatch': leave['tz_mismatch'],
                    'overtime_deductible': leave['overtime_deductible'],
                    'has_mandatory_day': leave['has_mandatory_day'],
                    'is_striked': leave['is_striked'],
                    'is_hatched': leave['is_hatched'],
                    'request_unit_hours': leave['request_unit_hours'],
                    'request_unit_half': leave['request_unit_half'],
                    'leave_type_support_document': leave['leave_type_support_document'],
                    'active': leave['active'],
                    'can_cancel': leave['can_cancel'],
                    'can_approve': leave['can_approve'],
                    'can_reset': leave['can_reset'],
                    'multi_employee': leave['multi_employee'],
                    'is_user_only_responsible': leave['is_user_only_responsible'],
                    'active_employee': leave['active_employee'],
                    'leave_type_increases_duration': leave['leave_type_increases_duration'],
                    'name': leave['name'],
                    'activity_type_icon': leave['activity_type_icon'],
                    'activity_summary': leave['activity_summary'],
                    'activity_exception_icon': leave['activity_exception_icon'],
                    'display_name': leave['display_name'],
                    'private_name': leave['private_name'],
                    'duration_display': leave['duration_display'],
                    'number_of_hours_text': leave['number_of_hours_text'],
                    'request_date_from': leave['request_date_from'],
                    'activity_date_deadline': leave['activity_date_deadline'],
                    'my_activity_date_deadline': leave['my_activity_date_deadline'],
                    'request_date_to': leave['request_date_to'],
                    'date_to': leave['date_to'],
                    'date_from': leave['date_from'],
                    'number_of_days': leave['number_of_days'],
                    'number_of_hours': leave['number_of_hours'],
                    'number_of_days_display': leave['number_of_days_display'],
                    'number_of_hours_display': leave['number_of_hours_display'],
                    'employee_overtime': leave['employee_overtime'],
                    'color': leave['color'],
                    'first_approver_id': first_approver_id.id if first_approver_id else False,
                    'second_approver_id': second_approver_id.id if second_approver_id else False,
                    'department_id': department_id.id if department_id else False,
                    'employee_id': employee_id.id if employee_id else False,
                    'holiday_status_id': holiday_status_id.id if holiday_status_id else False,
                    'parent_id': parent_id.id if parent_id else False,
                    'manager_id': manager_id.id if manager_id else False,
                    'category_id': category_id.id if category_id else False,
                    'leave_type_request_unit': leave['leave_type_request_unit'],
                    'request_hour_from': leave['request_hour_from'],
                    'request_date_from_period': leave['request_date_from_period'],
                    'holiday_type': leave['holiday_type'],
                    'activity_state': leave['activity_state'],
                    'validation_type': leave['validation_type'],
                    'activity_exception_decoration': leave['activity_exception_decoration'],
                    'tz': leave['tz'],
                    'state': leave['state'],
                    'request_hour_to': leave['request_hour_to'],
                    'report_note': leave['report_note'],
                    'notes': leave['notes'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    'source_id': leave['id'],
                    'tz_mismatch': leave['tz_mismatch'],
                    'overtime_deductible': leave['overtime_deductible'],
                    'has_mandatory_day': leave['has_mandatory_day'],
                    'is_striked': leave['is_striked'],
                    'is_hatched': leave['is_hatched'],
                    'request_unit_hours': leave['request_unit_hours'],
                    'request_unit_half': leave['request_unit_half'],
                    'leave_type_support_document': leave['leave_type_support_document'],
                    'active': leave['active'],
                    'can_cancel': leave['can_cancel'],
                    'can_approve': leave['can_approve'],
                    'can_reset': leave['can_reset'],
                    'multi_employee': leave['multi_employee'],
                    'is_user_only_responsible': leave['is_user_only_responsible'],
                    'active_employee': leave['active_employee'],
                    'leave_type_increases_duration': leave['leave_type_increases_duration'],
                    'name': leave['name'],
                    'activity_type_icon': leave['activity_type_icon'],
                    'activity_summary': leave['activity_summary'],
                    'activity_exception_icon': leave['activity_exception_icon'],
                    'display_name': leave['display_name'],
                    'private_name': leave['private_name'],
                    'duration_display': leave['duration_display'],
                    'number_of_hours_text': leave['number_of_hours_text'],
                    'request_date_from': leave['request_date_from'],
                    'activity_date_deadline': leave['activity_date_deadline'],
                    'my_activity_date_deadline': leave['my_activity_date_deadline'],
                    'request_date_to': leave['request_date_to'],
                    'date_to': leave['date_to'],
                    'date_from': leave['date_from'],
                    'number_of_days': leave['number_of_days'],
                    'number_of_hours': leave['number_of_hours'],
                    'number_of_days_display': leave['number_of_days_display'],
                    'number_of_hours_display': leave['number_of_hours_display'],
                    'employee_overtime': leave['employee_overtime'],
                    'color': leave['color'],
                    'first_approver_id': first_approver_id.id if first_approver_id else False,
                    'second_approver_id': second_approver_id.id if second_approver_id else False,
                    'department_id': department_id.id if department_id else False,
                    'employee_id': employee_id.id if employee_id else False,
                    'holiday_status_id': holiday_status_id.id if holiday_status_id else False,
                    'parent_id': parent_id.id if parent_id else False,
                    'manager_id': manager_id.id if manager_id else False,
                    'category_id': category_id.id if category_id else False,
                    'leave_type_request_unit': leave['leave_type_request_unit'],
                    'request_hour_from': leave['request_hour_from'],
                    'request_date_from_period': leave['request_date_from_period'],
                    'holiday_type': leave['holiday_type'],
                    'activity_state': leave['activity_state'],
                    'validation_type': leave['validation_type'],
                    'activity_exception_decoration': leave['activity_exception_decoration'],
                    'tz': leave['tz'],
                    'state': leave['state'],
                    'request_hour_to': leave['request_hour_to'],
                    'report_note': leave['report_note'],
                    'notes': leave['notes'],
                    'last_sync_date': fields.Datetime.now(),
                })

        # for timesheet in timesheets:
        #     existing_record = self.env['account.analytic.line'].search([('source_id', '=', timesheet['id'])])
        #     partner_id = False
        #     logging.info("<<<<<<<<<<<<<<< Project Partner ID >>>>>>>>>>>>>>>>>>>")
        #     if timesheet['partner_id']:
        #         logging.info(timesheet['partner_id'][0])
        #         partner, new_create = self.get_record('res.partner', timesheet['partner_id'][0], partner_fields, enterprise_models, enterprise_db_name, enterprise_uid, enterprise_api_pass)
        #         parent_id = False
        #         if partner['parent_id']:
        #             parent_id = self.env['res.partner'].sudo().search([('source_id', '=', partner['parent_id'])])
        #         if new_create:
        #             logging.info("<<<<<<<<<<<<<< Partner Details >>>>>>>>>>>>>>>>>>>>>")
        #             logging.info(partner)
        #
        #             partner_id =  self.env['res.partner'].create({
        #                 'name': partner['name'],
        #                 'display_name': partner['display_name'],
        #                 'company_type': partner['company_type'],
        #                 'country_code': partner['country_code'],
        #                 'active': partner['active'],
        #                 'company_name': partner['company_name'],
        #                 'type': partner['type'],
        #                 'street': partner['street'],
        #                 'street2': partner['street2'],
        #                 'city': partner['city'],
        #                 'zip': partner['zip'],
        #                 'phone': partner['phone'],
        #                 'mobile': partner['mobile'],
        #                 'email': partner['email'],
        #                 'vat': partner['vat'],
        #                 'parent_id': parent_id.id if parent_id else False,
        #                 'source_id': partner['id'],
        #                 'last_sync_date': datetime.now(),
        #             })
        #         else:
        #             partner_id = partner
        #
        #     project_id = False
        #     if timesheet['project_id']:
        #         project_rec = self.env['project.project'].sudo().search([('source_id','=',timesheet['project_id'][0])])
        #         if project_rec:
        #             project_id = project_rec
        #
        #     task_id = False
        #     if timesheet['task_id']:
        #         task_rec = self.env['project.task'].sudo().search([('source_id','=',timesheet['task_id'][0])])
        #         if task_rec:
        #             task_id = task_rec
        #     parent_task_id = False
        #     if timesheet['parent_task_id']:
        #         parent_task_rec = self.env['project.task'].sudo().search([('source_id','=',timesheet['parent_task_id'][0])])
        #         if parent_task_rec:
        #             parent_task_id = parent_task_rec
        #
        #     employee_id = False
        #     if timesheet['employee_id']:
        #         employee_rec = self.env['hr.employee'].sudo().search([('source_id','=',timesheet['employee_id'][0])])
        #         if employee_rec:
        #             employee_id = employee_rec
        #
        #     manager_id = False
        #     if timesheet['manager_id']:
        #         manager_rec = self.env['hr.employee'].sudo().search([('source_id','=',timesheet['manager_id'][0])])
        #         if manager_rec:
        #             manager_id = manager_rec
        #
        #     holiday_id = False
        #     if timesheet['holiday_id']:
        #         holiday_rec = self.env['hr.leave'].sudo().search([('source_id','=',timesheet['holiday_id'][0])])
        #         if holiday_rec:
        #             holiday_id = holiday_rec
        #
        #     if not existing_record:
        #         self.env['account.analytic.line'].sudo().create({
        #             'source_id': timesheet['id'],
        #             'date': timesheet['date'],
        #             'is_timesheet': 1,
        #             'project_id': project_id.id if project_id else False,
        #             'task_id': task_id.id if task_id else False,
        #             'name': timesheet['name'],
        #             'unit_amount': timesheet['unit_amount'],
        #             'readonly_timesheet': timesheet['readonly_timesheet'],
        #             'display_name': timesheet['display_name'],
        #             # 'ref': timesheet['ref'],
        #             'job_title': timesheet['job_title'],
        #             # 'code': timesheet['code'],
        #             'amount': timesheet['amount'],
        #             'category': timesheet['category'],
        #             'employee_id': employee_id.id if employee_id else False,
        #             'parent_task_id': parent_task_id.id if parent_task_id else False,
        #             'manager_id': manager_id.id if manager_id else False,
        #             'holiday_id': holiday_id.id if holiday_id else False,
        #             'partner_id': partner_id.id if parent_id else False,
        #             'last_sync_date': fields.Datetime.now(),
        #         })
        #     else:
        #         existing_record.sudo().write({
        #             'source_id': timesheet['id'],
        #             'date': timesheet['date'],
        #             'project_id': project_id.id if project_id else False,
        #             'task_id': task_id.id if task_id else False,
        #             'name': timesheet['name'],
        #             'unit_amount': timesheet['unit_amount'],
        #             'readonly_timesheet': timesheet['readonly_timesheet'],
        #             'display_name': timesheet['display_name'],
        #             # 'ref': timesheet['ref'],
        #             'job_title': timesheet['job_title'],
        #             # 'code': timesheet['code'],
        #             'amount': timesheet['amount'],
        #             'category': timesheet['category'],
        #             'employee_id': employee_id.id if employee_id else False,
        #             'parent_task_id': parent_task_id.id if parent_task_id else False,
        #             'manager_id': manager_id.id if manager_id else False,
        #             'holiday_id': holiday_id.id if holiday_id else False,
        #             'partner_id': partner_id.id if parent_id else False,
        #             'last_sync_date': fields.Datetime.now(),
        #         })

        for attendance in attendances:
            existing_record = self.env['hr.attendance'].search([('source_id', '=', attendance['id'])])

            employee_id = False
            if attendance['employee_id']:
                employee_rec = self.env['hr.employee'].sudo().search([('source_id','=',attendance['employee_id'][0])])
                if employee_rec:
                    employee_id = employee_rec

            department_id = False
            if attendance['department_id']:
                department_rec = self.env['hr.department'].sudo().search([('source_id','=',attendance['department_id'][0])])
                if department_rec:
                    department_id = department_rec

            if not existing_record:
                self.env['hr.attendance'].sudo().create({
                    'source_id': attendance['id'],
                    'out_country_name': attendance['out_country_name'],
                    'in_browser': attendance['in_browser'],
                    'in_ip_address': attendance['in_ip_address'],
                    'in_country_name': attendance['in_country_name'],
                    'in_city': attendance['in_city'],
                    'display_name': attendance['display_name'],
                    'out_browser': attendance['out_browser'],
                    'out_ip_address': attendance['out_ip_address'],
                    'out_city': attendance['out_city'],
                    'check_in': attendance['check_in'],
                    'check_out': attendance['check_out'],
                    'out_latitude': attendance['out_latitude'],
                    'in_latitude': attendance['in_latitude'],
                    'in_longitude': attendance['in_longitude'],
                    'overtime_hours': attendance['overtime_hours'],
                    'worked_hours': attendance['worked_hours'],
                    'out_longitude': attendance['out_longitude'],
                    'color': attendance['color'],
                    'employee_id': employee_id.id if employee_id else False,
                    'department_id': department_id.id if department_id else False,
                    'in_mode': attendance['in_mode'],
                    'out_mode': attendance['out_mode'],
                    'last_sync_date': fields.Datetime.now(),
                })
            else:
                existing_record.sudo().write({
                    # 'source_id': attendance['source_id'],
                    'out_country_name': attendance['out_country_name'],
                    'in_browser': attendance['in_browser'],
                    'in_ip_address': attendance['in_ip_address'],
                    'in_country_name': attendance['in_country_name'],
                    'in_city': attendance['in_city'],
                    'display_name': attendance['display_name'],
                    'out_browser': attendance['out_browser'],
                    'out_ip_address': attendance['out_ip_address'],
                    'out_city': attendance['out_city'],
                    'check_in': attendance['check_in'],
                    'check_out': attendance['check_out'],
                    'out_latitude': attendance['out_latitude'],
                    'in_latitude': attendance['in_latitude'],
                    'in_longitude': attendance['in_longitude'],
                    'overtime_hours': attendance['overtime_hours'],
                    'worked_hours': attendance['worked_hours'],
                    'out_longitude': attendance['out_longitude'],
                    'color': attendance['color'],
                    'employee_id': employee_id.id if employee_id else False,
                    'department_id': department_id.id if department_id else False,
                    'in_mode': attendance['in_mode'],
                    'out_mode': attendance['out_mode'],
                    'last_sync_date': fields.Datetime.now(),
                })



        self.env.cr.commit()

        # Updating the records, here we are sure that all dependent objects are created, so all many2one objects are created, so we can update all
        # self.update_records('resource.calendar', resource_calendars, resource_calendars_fields)
        # self.update_records('hr.department', departments, departments_fields)
        # self.update_records('hr.job', jobs, jobs_fields)
        # self.update_records('hr.employee', employees, employees_fields)
        # self.update_records('account.analytic.account', analytic_accounts, analytic_accounts_fields)
        # self.update_records('project.project', projects, projects_fields)

        # self.env.cr.commit()

        # Update the records in the enterprise : Last Sending Date & Sent = True

        # First : Get the ids
        # resource_calendar_ids = [record['id'] for record in resource_calendars]
        # department_ids = [record['id'] for record in departments]
        # job_ids = [record['id'] for record in jobs]
        # employee_ids = [record['id'] for record in employees]
        # analytic_account_ids = [record['id'] for record in analytic_accounts]
        # project_ids = [record['id'] for record in projects]

        # Second : Update in enterprise :




        dt = datetime.now()
        # self.update_enterprise_records('resource.calendar', resource_calendars, enterprise_models,
        #                                enterprise_db_name, enterprise_uid, enterprise_api_pass, dt)
        # self.update_enterprise_records('hr.department', departments, enterprise_models, enterprise_db_name,
        #                                enterprise_uid, enterprise_api_pass, dt)
        # self.update_enterprise_records('hr.job', jobs, enterprise_models, enterprise_db_name, enterprise_uid,
        #                                enterprise_api_pass, dt)
        # self.update_enterprise_records('hr.employee', employees, enterprise_models, enterprise_db_name,
        #                                enterprise_uid, enterprise_api_pass, dt)
        # self.update_enterprise_records('account.analytic.account', analytic_accounts, enterprise_models,
        #                                enterprise_db_name, enterprise_uid, enterprise_api_pass, dt)
        # self.update_enterprise_records('res.partner', partners, enterprise_models, enterprise_db_name,
        #                                enterprise_uid, enterprise_api_pass, dt)

        if projects:
            self.update_enterprise_records('project.project', projects, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if tasks:
            self.update_enterprise_records('project.task', tasks, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if task_types:
            self.update_enterprise_records('project.task.type', task_types, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
            # self.update_enterprise_records('account.analytic.line', timesheets, enterprise_models, enterprise_db_name,
            #                                enterprise_uid, enterprise_api_pass, dt)
        if employees:
            self.update_enterprise_records('hr.employee', employees, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if contracts:
            self.update_enterprise_records('hr.contract', contracts, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if attendances:
            self.update_enterprise_records('hr.attendance', attendances, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if leaves:
            self.update_enterprise_records('hr.leave', leaves, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if leave_types:
            self.update_enterprise_records('hr.leave.type', leave_types, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)
        if project_stages:
            self.update_enterprise_records('project.project.stage', project_stages, enterprise_models, enterprise_db_name,
                                           enterprise_uid, enterprise_api_pass, dt)

        self.sync_timesheets(timesheet_fields, enterprise_models, enterprise_db_name,
                                       enterprise_uid, enterprise_api_pass)

        # End integration logging
        self.log_integration_end()


    def update_records(self, model, source_records, fields_to_update):
        for record in source_records:
            source_id = record['id']
            existing_record = self.env[model].search([('source_id', '=', source_id)])

            if existing_record:
                vals = {
                    'last_sync_date': fields.Datetime.now(),
                }

                for field in fields_to_update:
                    field_info = self.env[model]._fields[field]
                    field_value = record.get(field)
                    if field_value is not False:
                        if field_info.type == 'many2one':
                            related_model = field_info.comodel_name
                            if isinstance(field_value, dict):  # Check if the field value is a dictionary
                                related_key, related_value = field_value.items()  # Fetch key and value of the many2one field
                                related_record = self.env[related_model].search([(source_id, '=', related_key)])

                                if related_record:
                                    vals[field] = related_record.id
                            else:
                                related_record = self.env[related_model].search(
                                    [('source_id', '=', field_value[0])])  # Replace 'key_field' with the actual field name
                                    # [('source_id', '=', field_value[0])])  # Replace 'key_field' with the actual field name
                                if related_record:
                                    vals[field] = related_record.id
                        else:
                            vals[field] = field_value

                existing_record.write(vals)
            else:
                logging.info(f"Record with source_id {source_id} not found in {model}")

    def update_enterprise_records(self, model, record_ids, enterprise_models, enterprise_db_name, enterprise_uid,
                                  enterprise_api_pass, dt):
        ids_to_update = [record['id'] for record in record_ids]  # Extract IDs from dictionaries

        if ids_to_update:
            try:
                logging.info("Updating records:", ids_to_update)
                enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass, model, 'write',
                                             [ids_to_update, {'sent': True, 'last_sending_date': dt, }])
            except Exception as e:
                logging.info("Error:", e)

    def get_record(self, model, record_id, model_fields, enterprise_models, enterprise_db_name, enterprise_uid,
                                  enterprise_api_pass):
        logging.info("<<<<<<<<<<<<< Get records Args >>>>>>>>>>>>>>>>")
        logging.info(model)
        logging.info(record_id)
        logging.info(type(record_id))

        partner_id = self.env[model].sudo().search([('source_id','=',record_id)])
        if partner_id:
            return partner_id, False
        else:
            try:
                logging.info("Fetching record against id:", str(record_id))
                partner = enterprise_models.execute_kw(enterprise_db_name, enterprise_uid, enterprise_api_pass,
                                                     model, 'search_read',
                                                     [[('id', '=', record_id)]],
                                                     {'fields': model_fields})
                return partner[0], True
            except Exception as e:
                logging.info("Error:", e)


    def sync_timesheets(self, timesheet_fields, enterprise_models, enterprise_db_name, enterprise_uid, enterprise_api_pass):
        domain = [('sync', '=', True), ('sent', '=', False),('source_id','=',False)]
        timesheets = self.env['account.analytic.line'].sudo().search_read(
            domain = domain,
            fields = timesheet_fields
        )
        for timesheet in timesheets:
            logging.info("<<<<<<<<<< Time Sheet Dict >>>>>>>>>>>>>>>>>>>")
            logging.info(timesheet)
            logging.info(timesheet['employee_id'][0])
            employee_id = self.env['hr.employee'].sudo().search([('id','=',timesheet['employee_id'][0])])
            project_id = self.env['project.project'].sudo().search([('id','=',timesheet['project_id'][0])])
            task_id = False
            if timesheet['task_id']:
                task_id = self.env['project.task'].sudo().search([('id','=',timesheet['task_id'][0])])
                if task_id.source_id:
                    task_id = task_id.source_id
            logging.info(employee_id)
            if employee_id.source_id:
                employee_id = employee_id.source_id
                if project_id.source_id:
                    project_id = project_id.source_id
                    try:
                        time_sheet_data = {
                            'date': timesheet['date'],
                            'name': timesheet['name'],
                            'unit_amount': timesheet['unit_amount'],
                            'readonly_timesheet': timesheet['readonly_timesheet'],
                            'display_name': timesheet['display_name'],
                            'job_title': timesheet['job_title'],
                            'amount': timesheet['amount'],
                            'category': timesheet['category'],
                            'employee_id': employee_id,
                            'project_id': project_id,
                            'task_id': task_id,
                            'sent': True,
                            'last_sending_date': datetime.now()
                        }

                        synced_timesheet_record = enterprise_models.execute_kw(
                            enterprise_db_name,
                            enterprise_uid,
                            enterprise_api_pass,
                            'account.analytic.line',
                            'create',
                            [time_sheet_data])
                        logging.info (f"Created timesheet for {timesheet['name']} in Odoo 17.")

                        # synced_timesheet_record.sent = True
                        # synced_timesheet_record.last_sending_date = datetime.now()
                        timesheet_rec = self.env['account.analytic.line'].sudo().search([('id','=',timesheet['id'])])
                        timesheet_rec.source_id = synced_timesheet_record
                        timesheet_rec.last_sync_date = datetime.now()
                        # timesheet.source_id = synced_timesheet_record
                        # timesheet.last_sync_date = datetime.now()
                        return synced_timesheet_record
                    except Exception as e:
                        logging.info (f"Error creating timesheet in Odoo 17: {e}")
                        return None




