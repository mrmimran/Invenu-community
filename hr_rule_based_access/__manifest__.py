# -*- coding: utf-8 -*-
{
    'name': "hr_rule_based_access",

    'summary': "Manage access control for HR records based on roles",

    'description': """
        This module implements role-based access restrictions:
        - Employees can see only their own records.
        - Managers can see records of their department.
        - HR and Admin can access all records.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Human Resources',
    'version': '0.1',

     'depends': ['base','hr','hr_contract','hr_holidays','hr_attendance','hr_appraisal', ],

    'data': [
        # 'security/ir.model.access.csv',  # Access control definitions
        # 'views/security_group_views.xml', # Views for security groups
        # 'views/security_rule_views.xml',  # Views for security rules
        # 'views/hr_contract_views.xml',     # HR contract views with access control
        # 'security/group_hr_employee_access.xml',
        'security/group_enterprise_hr_access.xml',


    ],
    'demo': [
        'demo/demo.xml',
    ],
}
