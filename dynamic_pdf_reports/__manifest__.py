# -*- coding: utf-8 -*-
{
    'name': 'Dynamic Pdf Reports',
    'category': 'Reports',
    'version': '1.1',
    'summary': 'This module helps to get the dynamic names on pdf reports while downloading.',
    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'license': 'AGPL-3',
    'description': 'Manage printing multiple reports with dynamic pdf names.',
    'depends': ['hr', 'report'],
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_report_view.xml',
    ],

    'images': ['static/description/banner.jpg'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
