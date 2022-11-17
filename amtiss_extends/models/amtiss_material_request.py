from odoo import models, fields, api, _


class AmtissMaterialRequestInherited331(models.Model):
    _inherit = "amtiss.material.request"
                        
    
    @api.onchange("picking_location_id")
    def _compute_picking_location_id(self):
        self.ensure_one()
        for line in self.amtiss_material_request_line_ids:
            line.write({"picking_location_id" : self.picking_location_id})
    
    
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
        
    
    def button_process(self):
        self.ensure_one()
        wizard = self.env["amtiss.process.confirmation"].create({"amtiss_material_request_id" : self.id})
        
        
        return {
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'amtiss.process.confirmation',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
              }
        
        
        
    def continue_process(self):
        if not self.amtiss_material_request_line_ids:
            raise UserError(_("Please add the Material Request Lines (Resources) first, then you can process."))
        
        action_data = {}
        asset_id = self.asset_id.id if self.asset_id else None
        for amtiss_material_request_line_id in self.amtiss_material_request_line_ids:
            if amtiss_material_request_line_id.status_request_line == "Draft":
                # Creation of Purchase Request
                if amtiss_material_request_line_id.status == 'Purchase':
                    self.env['purchase.request'].create({
                        'requested_by': self.env.user.id,
                        'line_ids':[(0, 0, {
                            'product_id': amtiss_material_request_line_id.name.id,
                            'product_qty': amtiss_material_request_line_id.quantity,
                        })],
                        'amtiss_material_request_id' : self.id,
                        'asset_id' : asset_id
                    })
        
                # Creation of Picking, Delivery Orders
                elif amtiss_material_request_line_id.status == 'Picking':
                    # remove the checking if stock = 0
                    # if amtiss_material_request_line_id.stock_on_picking_location_id == 0:
                    #     raise UserError(_("Since for the product %s, the Quantity available at Picking Location is 0. You can't select Picking status." % (amtiss_material_request_line_id.name.display_name)))
                    
                    if amtiss_material_request_line_id.picking_location_id.warehouse_id.out_type_id.default_location_dest_id:
                        location_dest_id = amtiss_material_request_line_id.picking_location_id.warehouse_id.out_type_id.default_location_dest_id.id
                    else:
                        location_dest_id, supplierloc = self.env['stock.warehouse']._get_partner_locations()
                    
                    
                    if not action_data.get('picking') :
                        stock_picking_id = self.env['stock.picking'].create({
                            'picking_type_id':amtiss_material_request_line_id.picking_location_id.warehouse_id.out_type_id.id,
                            'location_id': amtiss_material_request_line_id.picking_location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'amtiss_material_request_id' : self.id,
                            'asset_id' : asset_id
                        })
                        action_data['picking'] = stock_picking_id
                        
                    if action_data.get('picking'):                    
                        action_data.get('picking').move_ids_without_package = [(0, 0, {
                            'name': stock_picking_id.name,
                            'product_id': amtiss_material_request_line_id.name.id,
                            'product_uom': amtiss_material_request_line_id.uom_id.id,
                            'product_uom_qty': amtiss_material_request_line_id.quantity,
                            'location_id': stock_picking_id.location_id.id,
                            'location_dest_id': stock_picking_id.location_dest_id.id
                        })]
        
                # Creation of Picking, Internal Transfer
                elif amtiss_material_request_line_id.status == 'Transfer':
                    picking = None
                    if not action_data.get('transfer') :
                        stock_picking_id = self.env['stock.picking'].create({
                            'picking_type_id':amtiss_material_request_line_id.picking_location_id.warehouse_id.int_type_id.id,
                            'location_id': amtiss_material_request_line_id.source_picking_location_id.id,
                            'location_dest_id': amtiss_material_request_line_id.picking_location_id.id,
                            'amtiss_material_request_id' : self.id,
                            'asset_id' : asset_id
                        })
                        action_data['transfer'] = [stock_picking_id]
                        picking = stock_picking_id
                    
                    else :
                        for tf in action_data['transfer']:
                            if tf.location_id.id == amtiss_material_request_line_id.source_picking_location_id.id and tf.location_dest_id.id == amtiss_material_request_line_id.picking_location_id.id:
                                picking = tf
                                break
                        if not picking :
                            stock_picking_id = self.env['stock.picking'].create({
                            'picking_type_id':amtiss_material_request_line_id.picking_location_id.warehouse_id.int_type_id.id,
                            'location_id': amtiss_material_request_line_id.source_picking_location_id.id,
                            'location_dest_id': amtiss_material_request_line_id.picking_location_id.id,
                            'amtiss_material_request_id' : self.id,
                            'asset_id' : asset_id
                        })
                            action_data['transfer'].append(stock_picking_id)
                            picking = stock_picking_id
                        
                    if picking:
                        picking.move_ids_without_package = [(0, 0, {
                            'name': stock_picking_id.name,
                            'product_id': amtiss_material_request_line_id.name.id,
                            'product_uom': amtiss_material_request_line_id.uom_id.id,
                            'product_uom_qty': amtiss_material_request_line_id.quantity,
                            'location_id': stock_picking_id.location_id.id,
                            'location_dest_id': stock_picking_id.location_dest_id.id
                        })]
                
                amtiss_material_request_line_id.status_request_line = 'Processed'
            
                                
        self.state = 'Approved'
        return {}