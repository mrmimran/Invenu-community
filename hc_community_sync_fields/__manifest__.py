# -*- coding: utf-8 -*-
{
    'name': "API Integration for Data",

    'summary': "Integrate data through APIs into Odoo platform.",

    'description': """
        This module allows integration of HR data using APIs into the Odoo platform. It enables fetching employee information, jobs, and departments through API calls.

        Features:
        - Fetch and display employee details.
        - Retrieve and view job information.
        - Access and display department data.

        Note: This module requires proper configuration of API endpoints.
    """,

    'author': "Your Company",
    'website': "https://www.yourcompany.com",

    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base','hr','project','account', 'hr_timesheet', 'hr_holidays','hr_contract','hr_attendance'],

    'data': [
        # 'views/cron_data.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
