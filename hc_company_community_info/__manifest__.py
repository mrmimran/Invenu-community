# -*- coding: utf-8 -*-
{
    'name': "ERP Synchronization",

    'summary': "Module for synchronizing data between Odoo instances and external APIs.",


    'description': "This module enables data synchronization between Odoo instances and external APIs.",

    'author': "Your Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/security_groups.xml',
        'views/views.xml',
        'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
