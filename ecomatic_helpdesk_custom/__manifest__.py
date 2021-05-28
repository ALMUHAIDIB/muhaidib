# -*- coding: utf-8 -*-
{
    'name': "ecomatic_helpdesk_custom",
    'depends': ['base', 'ecomatic_res_partner_custom', 'helpdesk'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence.xml',
        'views/helpdesk_views.xml',
        'views/employee_views.xml',
        'views/res_users_views.xml',
        'views/helpdesk_groups_readonly_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}