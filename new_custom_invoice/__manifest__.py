# -*- coding: utf-8 -*-
{
    'name': "new_custom_invoice",

    'summary': """
        new custom invoice template for customer invoices""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Centione",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'product', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/account_invoice.xml',
        'views/product.xml',
        'views/views.xml',
        'views/stock.xml',
        'views/sale.xml',
        'views/report_payment_receipt.xml',
    ],
}