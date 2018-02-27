# -*- coding: utf-8 -*-
{
    'name': 'Dynamic Pdf Reports',
    'category': '',
    'version': '1.1',
    'website': 'http://www.aktivsoftware.com',
    'author': 'Aktiv Software',
    'license': 'AGPL-3',
    'description': 'Manage printing multiple reports with dynamic pdf names.',
    'depends': ['hr', 'web', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/dynamic_report_view.xml',
    ],

    'images': [],
    'images': ['static/description/banner.jpg'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
