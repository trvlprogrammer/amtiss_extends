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
    'depends': ['amtiss_material_req','amtiss_assignment','amtiss_asset','purchase'],
    'data': [
        'security/ir.model.access.csv',
                
        'views/material_request.xml',
        'views/stock_picking.xml',
        'views/material_request_line.xml',
        
        'wizard/amtiss_action_set.xml',        
        'wizard/amtiss_product_exchange.xml',
        'wizard/amtiss_process_confirmation.xml'
        
    ],
}
