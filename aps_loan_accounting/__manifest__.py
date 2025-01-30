# -*- coding: utf-8 -*-
{
    'name': 'Enterprise Open HRMS Loan Accounting',
    'version': '17.0.1.0.0',
    'summary': 'Open HRMS Loan Accounting',
    'description': """
        Create accounting entries for loan requests.
        """,
    'category': 'Generic Modules/Human Resources',
    'author': "Amjid Waxir",
    'company': 'Altapete Solutions',
    'maintainer': 'Altapete Solutions',
    'website': "http://www.altapetesolutions.com/",
    'depends': [
        'base', 'payroll', 'hr', 'account', 'aps_hr_payroll_extension',
        'account', 'aps_ent_loan'
    ],
    'data': [
        'views/hr_loan_config.xml',
        'views/hr_loan_acc.xml',
        'views/hr_adv_acc.xml',
        'views/hr_adv_config.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
}
