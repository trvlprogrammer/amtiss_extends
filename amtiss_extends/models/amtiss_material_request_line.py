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
                
            
    @api.depends('stock_quant_ids')
    def _compute_quantities_at_locations_mapped(self):
        for record in self:
            quantities_at_locations_mapped = "<ul style='list-style-type: none;overflow: hidden;'>"
            for stock_quant_id in record.stock_quant_ids:
                if stock_quant_id.quantity > 0 and not stock_quant_id.location_id.scrap_location:
                    if stock_quant_id.inventory_quantity_auto_apply:
                        quantities_at_locations_mapped += \
                            "<li style='border: 1px solid #eee;background-color: #eee;float: left;padding: 2px 5px;margin: 3px;border-radius: 10px;'>" + \
                                str(stock_quant_id.inventory_quantity_auto_apply) + " @ " + \
                                str(stock_quant_id.location_id.display_name) + \
                            "</li>"
            quantities_at_locations_mapped += '</ul>'
            record.quantities_at_locations_mapped = quantities_at_locations_mapped
            
            
        