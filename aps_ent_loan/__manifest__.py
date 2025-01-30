# -*- coding: utf-8 -*-
{
    'name': 'Enterprise Open Loan Management',
    'version': '17.0.1.0.0',
    'summary': 'Manage Loan Requests',
    'description': """Helps you to manage Loan Requests of your company's 
     staff.""",
    'category': 'Generic Modules/Human Resources',
    'author': "Altapete Solutions",
    'company': 'Altapete Solutions',
    'maintainer': 'Altapete Solutions',
    'website': "http://www.altapetesolutions.com/",
    'depends': [
        'base', 'payroll', 'hr', 'account', 'aps_hr_payroll_extension',
    ],
    'data': [
        'data/salary_rule_loan.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_loan_seq.xml',
        'views/hr_loan.xml',
        'views/hr_payroll.xml',
        'views/hr_advance.xml',
        'views/hr_payroll_advance.xml',
        'views/hr_advance_seq.xml',
        'views/new_payroll.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
