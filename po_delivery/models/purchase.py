# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    number_of_shipments = fields.Integer(string='Number Of shipments', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    shipment_ids = fields.One2many('serial.qty.shipment', 'po_id')

    @api.constrains('shipment_ids')
    def shipment_ids_constrain(self):
        if self.shipment_ids:
            if sum(self.shipment_ids.mapped('qty')) > sum(self.order_line.mapped('product_qty')):
                raise ValidationError("Shipment Quantity Should be Equal Product Quantity")
            elif sum(self.shipment_ids.mapped('qty')) < sum(self.order_line.mapped('product_qty')):
                raise ValidationError("Shipment Quantity Should be Equal Product Quantity")

    @api.constrains('number_of_shipments', 'order_line')
    def shipment_create(self):
        if self.number_of_shipments and self.order_line:
            vals= {}
            serial_qty_obj = self.env['serial.qty.shipment']
            serial = 1
            for i in range(self.number_of_shipments):
                for line in self.order_line:
                    if round(line.product_qty / self.number_of_shipments, 2) * self.number_of_shipments != line.product_qty:
                        raise ValidationError('The Number of quantity of {0} Must be dividable on the number of shipments')

                    else:
                        vals['product_id'] = line.product_id.id
                        vals['qty'] = line.product_qty / self.number_of_shipments
                        vals['serial'] = serial
                        new_obj = serial_qty_obj.new(vals)
                        serial_qty_obj += new_obj
                serial += 1

            self.shipment_ids = serial_qty_obj

    @api.multi
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                # pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                for i in range(order.number_of_shipments):
                    # if not pickings:
                    res = order._prepare_picking()
                    picking = StockPicking.create(res)
                    picking.write({
                        'serial_number': i+1
                    })
                    # else:
                    # picking = pickings[0]
                    moves = order.order_line._create_stock_moves(picking)

                    moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                    seq = 0
                    for move in sorted(moves, key=lambda move: move.date_expected):
                        seq += 5
                        move.sequence = seq
                    moves._action_assign()
                    picking.message_post_with_view('mail.message_origin_link',
                                                   values={'self': picking, 'origin': order},
                                                   subtype_id=self.env.ref('mail.mt_note').id)
        return True





class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    def get_shipment_qty(self,product,serial):
        for record in self:
            for line in record.order_id.shipment_ids:
                if line.product_id.id == product.id and line.serial == int(serial):
                    return line.qty


    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        shipment_lines = self.env['serial.qty.shipment'].search([('po_id', '=', self[0].order_id.id),
                                                                 ('serial', '=', picking.serial_number)])
        for record in shipment_lines:
            for line in self:
                if line.product_id.id == record.product_id.id:
                    for val in line._prepare_stock_moves(picking):
                        done += moves.create(val)
        return done

    @api.multi
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        price_unit = self._get_stock_move_price_unit()
        for move in self.move_ids.filtered(
                lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
            qty += move.product_uom._compute_quantity(move.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
        template = {
            'name': self.name or '',
            'product_id': self.product_id.id,
            'product_uom': self.product_uom.id,
            'date': self.order_id.date_order,
            'date_expected': self.date_planned,
            'location_id': self.order_id.partner_id.property_stock_supplier.id,
            'location_dest_id': self.order_id._get_destination_location(),
            'picking_id': picking.id,
            'partner_id': self.order_id.dest_address_id.id,
            'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
            'state': 'draft',
            'purchase_line_id': self.id,
            'company_id': self.order_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.order_id.picking_type_id.id,
            'group_id': self.order_id.group_id.id,
            'origin': self.order_id.name,
            'route_ids': self.order_id.picking_type_id.warehouse_id and [
                (6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
        }
        diff_quantity = self.product_qty - qty
        if float_compare(diff_quantity, 0.0, precision_rounding=self.product_uom.rounding) > 0:
            quant_uom = self.product_id.uom_id
            get_param = self.env['ir.config_parameter'].sudo().get_param
            if self.product_uom.id != quant_uom.id and get_param('stock.propagate_uom') != '1':
                # product_qty = self.product_uom._compute_quantity(diff_quantity, quant_uom, rounding_method='HALF-UP')
                product_qty = self.get_shipment_qty(self.product_id)
                template['product_uom'] = quant_uom.id
                template['product_uom_qty'] = product_qty
            else:
                diff_quantity = self.get_shipment_qty(self.product_id, picking.serial_number)
                template['product_uom_qty'] = diff_quantity
            res.append(template)
        return res

