# -*- coding: utf-8 -*-
{
    'name': "mmm_salesperson_custom",

    'summary': """
    SalesPerson Based On Company On partner In Sale Cycle
    """,

    'author': "Centione",
    'website': "http://www.centione.com",


    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ]
}
