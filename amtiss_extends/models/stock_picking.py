from odoo import models, fields, api, _


class StockPickingInherited331(models.Model):
    _inherit = "stock.picking"
    
    amtiss_material_request_id = fields.Many2one(
        string='MR ID',
        comodel_name='amtiss.material.request'
    )
    asset_id = fields.Many2one(comodel_name='amtiss.asset', string="Asset ID")