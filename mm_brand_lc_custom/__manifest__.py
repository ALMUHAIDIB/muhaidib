# -*- coding: utf-8 -*-
{
    'name': "mm_brand_lc_custom",

    'author': "Centione",
    'website': "http://www.centione.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','landed_cost_customizations'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_inherit.xml',
        'views/purchase_search_inherit.xml',
        'views/account_payment_inherit.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}