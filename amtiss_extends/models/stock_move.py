from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockMoveInherited331(models.Model):
    _inherit = "stock.move"
    
    
    qty_issued = fields.Float(string="Issued")
    
    @api.model
    def create(self,vals):        
        res = super(StockMoveInherited331,self).create(vals)   
        if res.qty_issued == 0:     
            res.qty_issued = res.product_uom_qty
        
        if res.qty_issued > res.product_uom_qty:
            raise UserError("Quantity issued can not be greater than demand")
        
        return res

    def write(self,vals):
        res = super(StockMoveInherited331,self).write(vals)   
        for record in self:
            if record.qty_issued > record.product_uom_qty:
                raise UserError("Quantity issued can not be greater than demand")
            
        return res