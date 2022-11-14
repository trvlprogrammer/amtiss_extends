# -*- coding: utf-8 -*-
{
    'name': "Amtiss Extends",

    'summary': """
        Amtiss Extends""",

    'description': """
        Amtiss Extends
    """,

    'author': "Alfatih Ridho NT",
    'website': "alfatihridhont@gmail.com",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['amtiss_material_req','amtiss_assignment','amtiss_asset'],
    'data': [
        'views/material_request.xml',
        'wizard/amtiss_product_exchange.xml',
        'views/material_request_line.xml',
        'wizard/amtiss_action_set.xml',
        'security/ir.model.access.csv',
    ],
}
