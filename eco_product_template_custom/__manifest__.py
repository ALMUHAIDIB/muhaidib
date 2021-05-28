# -*- coding: utf-8 -*-
{
    'name': "ECO Product Template Custom",
    'depends': ['base', 'product', 'helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
