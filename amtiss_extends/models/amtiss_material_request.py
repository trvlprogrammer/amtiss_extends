from odoo import models, fields, api, _


class AmtissMaterialRequestInherited331(models.Model):
    _inherit = "amtiss.material.request"
                        
    def write(self, vals):
        res = super(AmtissMaterialRequestInherited331,self).write(vals)            
        # change picking_id in request line based on material request picking id
        for line in self.amtiss_material_request_line_ids:
            line.write({"picking_location_id" : vals.get("picking_location_id")})
        return res
    
    
    def button_set_actiont(self):
        self.ensure_one()
        wizard = self.env["amtiss.action.set.wizard"].create({"amtiss_material_request_id" : self.id})
        
        
        return {
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'amtiss.action.set.wizard',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
              }