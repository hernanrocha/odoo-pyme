# -*- coding:utf-8 -*-

{
    'name': 'Gestion de PYME',
    'category': 'Sales/Sales',
    'version': '1.0.1.0.0',
    'sequence': 1,
    'author': 'Hernan Rocha',
    'summary': 'Sistema de gestion simplificado para PYMEs',
    'description': "",
    'depends': [
        'contacts',
        'mail',
        'purchase',
        'sale',
        'account',
        'stock'
    ],
    'data': [
        'views/mail_views.xml',
        'views/contacts_views.xml',
        'views/inventory_views.xml',
        'views/product_views.xml',
        'views/purchase_views.xml',
        'views/sale_views.xml',
    ],
    'images': [],
    'application': True,
}
