from odoo import models, fields, api, _


class AmtissMaterialRequestLineInherited331(models.Model):
    _inherit = "amtiss.material.request.line"
    
    status_request_line = fields.Selection(
        string='Status',
        selection=[
            ('Draft', 'Draft'),
            ('Processed', 'Processed'),
            ('Issued', 'Issued'),
            ('Canceled', 'Canceled'),
        ], default='Draft',)
                    
            
