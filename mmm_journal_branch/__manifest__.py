# -*- coding: utf-8 -*-
{
    'name': "MMM Journal Branch",
    'depends': ['base', 'account', 'stock_account', 'stock', 'mm_brand_lc_custom'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}