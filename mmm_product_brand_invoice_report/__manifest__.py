# -*- coding: utf-8 -*-
{
    'name': "MMM Product Brand Invoice Report",
    'depends': ['base', 'product', 'account', 'mm_brand_lc_custom', 'sale', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}