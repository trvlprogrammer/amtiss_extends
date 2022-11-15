from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AmtissProductExchangeInherited(models.TransientModel):
    _name = "amtiss.process.confirmation"
    
    amtiss_material_request_id = fields.Many2one("amtiss.material.request", string="MR ID")
    
    
    def button_process(self):
        self.amtiss_material_request_id.continue_process()