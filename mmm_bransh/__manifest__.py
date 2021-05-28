# -*- coding: utf-8 -*-
{
    'name': "mmm_bransh",



    'author': "Centione",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_form_view.xml',
        'views/res_partner_tree_view.xml',
        'views/res_partner_kanban_view_inherit.xml',
        'views/sale_order_form_inherit.xml',
        'views/account_invoice_inherit.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}