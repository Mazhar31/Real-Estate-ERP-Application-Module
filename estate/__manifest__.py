{
    'name': "Real-Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mazhar Shafiq",
    'category': "Category",
    'description': """
    This is a test module of Real-Estate Management!
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offer_views.xml',

        'views/estate_menus.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}