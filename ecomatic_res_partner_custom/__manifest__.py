# -*- coding: utf-8 -*-
{
    'name': "ecomatic_res_partner_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk', 'product', 'sale', 'contacts', 'eco_product_template_custom', 'sale_stock'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/log_call_wizard_view.xml',
        'views/views.xml',
        'views/res_users_inherit.xml',
        'views/templates.xml',
        'views/helpdesk_views.xml',
        'views/res_partner_inherit.xml',
        'views/rel_product_partner.xml',
        'views/about_us_views.xml',
        'views/log_call_views.xml',
        'views/res_vendor_views.xml',
        'views/product_template.xml',
        'views/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}