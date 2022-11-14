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
    
# class productProductInherit(models.Model):
#     _inherit = "product.product"
#
#     amtiss_product_exchange_id = fields.Many2one("amtiss.product.exchange", string="amtiss_product_exchange_id")