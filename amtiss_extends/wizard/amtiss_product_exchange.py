from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AmtissProductExchangeInherited(models.TransientModel):
    _inherit = "amtiss.product.exchange"
    
    selected_product_ids = fields.Many2many(
        "product.product","amtis_product_exchange_rel","product_exchange_id", "product_id",
        string="Selected Products"
    )
    
    
    @api.onchange('current_product_id')
    def _onchange_current_product_ids(self):
        for rec in self:
            if rec.current_product_id:
                current_product_variant_ids = self.env['product.product'].search([
                    ('product_tmpl_id', '=', rec.current_product_id.product_tmpl_id.id),
                    ('id', '!=', rec.current_product_id.id),
                ], 
                offset=0,                   #int
                limit=None,                 #int
                order=None,                 #string
                )
                return {
                    'domain': {
                        'selected_product_ids': [('id', 'in', current_product_variant_ids.ids)]
                    }
                }
                
                
    def action_replace_material_request_line(self):
        if len(self.selected_product_ids) > 1:
            raise UserError("You only can choose one product variant")  
        elif len(self.selected_product_ids) == 0:
            raise UserError("You need to choose one product variant")
        
        self.selected_product_id = self.selected_product_ids[0]
        
        return super(AmtissProductExchangeInherited,self).action_replace_material_request_line()
    