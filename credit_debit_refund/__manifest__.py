# -*- coding: utf-8 -*-
{
    'name': "Credit Debit and Refund",

    'summary': """
        credit and debit and refund notes""",

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
    'depends': ['base', 'account', 'product', 'new_custom_invoice'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product.xml',
        'wizards/debit.xml',
        'wizards/credit.xml',
        'views/account_invoice.xml',
        'reports/credit_note.xml',
        'reports/debit_note.xml',
    ],
}