from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AmtissProductExchangeInherited(models.TransientModel):
    _inherit = "amtiss.product.exchange"
    
    selected_product_ids = fields.One2many(
        "amtiss.product.exchange.detail","product_exchange_id",
        string="Selected Products"
    )
    
                
    def action_replace_material_request_line(self):
        if len(self.selected_product_ids) > 1:
            raise UserError("You only can choose one product variant")  
        elif len(self.selected_product_ids) == 0:
            raise UserError("You need to choose one product variant")
        
        self.selected_product_id = self.selected_product_ids[0].name
        
        return super(AmtissProductExchangeInherited,self).action_replace_material_request_line()
    
    
class AmtissProductExchangeDetail(models.TransientModel):
    _name ="amtiss.product.exchange.detail"
    
    product_exchange_id = fields.Many2one("amtiss.product.exchange", string="Product Exchange")
    name = fields.Many2one(string='Resource', comodel_name='product.product')
    standard_price = fields.Float(string='Standard Price', related='name.standard_price')
    uom_id = fields.Many2one(string='UoM', comodel_name='uom.uom', related='name.uom_id')
    qty_available = fields.Float(string="QoH",comodel_name='qty_available')
    quantities_at_locations_mapped = fields.Html(
        string='Qty At Other Warehouses',
        compute='_compute_quantities_at_locations_mapped',
    )
    
    @api.onchange('product_exchange_id','product_exchange_id.current_product_id', 'name')
    def _onchange_current_product_ids(self):
        for rec in self:
            if rec.product_exchange_id:
                current_product_variant_ids = self.env['product.product'].search([
                    ('product_tmpl_id', '=', rec.product_exchange_id.current_product_id.product_tmpl_id.id),
                    ('id', '!=', rec.product_exchange_id.current_product_id.id),
                ], 
                offset=0,                   #int
                limit=None,                 #int
                order=None,                 #string
                )
                return {
                    'domain': {
                        'name': [('id', 'in', current_product_variant_ids.ids)]
                    }
                }
                
                
    def get_quantity_by_location_id_and_product_id(self, products_id, location_id):
        quantity = 0.0
        stock_quant_ids = self.env['stock.quant'].search([
            ('product_id', '=', products_id.id),
            ('location_id', '=', location_id.id),
        ], 
        offset=0,                   #int
        limit=1,                 #int
        order=None,                 #string
        )
        if stock_quant_ids:
            quantity = stock_quant_ids.inventory_quantity_auto_apply
        return quantity
                
    @api.depends('picking_location_id')
    def _compute_stock_on_picking_location_id(self):
        for record in self:
            record.stock_on_picking_location_id = record.get_quantity_by_location_id_and_product_id(
                products_id= record.name,
                location_id= record.picking_location_id
            )
    
            
    @api.depends('name')
    def _compute_quantities_at_locations_mapped(self):            
        for record in self:
            quantities_at_locations_mapped = "<ul style='list-style-type: none;overflow: hidden;'>"
            for stock_quant_id in self.env["stock.quant"].search([("product_id","=",record.name.id)]):
                if stock_quant_id.quantity > 0 and not stock_quant_id.location_id.scrap_location:
                    if stock_quant_id.inventory_quantity_auto_apply:
                        quantities_at_locations_mapped += \
                            "<li style='border: 1px solid #eee;background-color: #eee;float: left;padding: 2px 5px;margin: 3px;border-radius: 10px;'>" + \
                                str(stock_quant_id.inventory_quantity_auto_apply) + " @ " + \
                                str(stock_quant_id.location_id.display_name) + \
                            "</li>"
            quantities_at_locations_mapped += '</ul>'
            record.quantities_at_locations_mapped = quantities_at_locations_mapped
    