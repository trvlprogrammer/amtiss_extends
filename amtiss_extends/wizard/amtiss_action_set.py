from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AmtissActionSet(models.TransientModel):
    _name = "amtiss.action.set.wizard"
    
    amtiss_material_request_id = fields.Many2one(
        string='Material Request',
        comodel_name='amtiss.material.request',
        readonly=True,
    )
    
    action = fields.Selection(
        string='Status',
        selection=[
            ('Picking', 'Picking'),
            ('Purchase', 'Purchase'),
            ('Transfer', 'Transfer'),
        ], default='Picking',)
    
    request_line_ids = fields.Many2many(
        "amtiss.material.request.line","amtiss_action_set_rel","action_id", "request_line_id",
        string="Resource"
    )
    
    source_picking_location_id = fields.Many2one(string='Location', comodel_name='stock.location',)
    
    
    
    @api.onchange('current_product_id')
    def _onchange_current_product_ids(self):
        for rec in self:
            if rec.amtiss_material_request_id:
                request_line_ids = self.env['amtiss.material.request.line'].search([
                    ('amtiss_material_request_id', '=', rec.amtiss_material_request_id.id)
                ], 
                offset=0,                   #int
                limit=None,                 #int
                order=None,                 #string
                )
                return {
                    'domain': {
                        'request_line_ids': [('id', 'in', request_line_ids.ids)]
                    }
                }
                
    # function to set action to request material line            
    def set_action(self):
        self.ensure_one()
        for record in self.request_line_ids:
            record.status = self.action
                        
            if self.action == "Transfer":
                record.source_picking_location_id = self.source_picking_location_id.id