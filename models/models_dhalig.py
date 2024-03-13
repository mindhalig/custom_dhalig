from odoo import api, models, fields,_
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    request_vendor = fields.Many2one(
                    'res.partner', 
                     string="Request Vendor")
    no_kontrak = fields.Char(
                    "No Kontrak")
    with_po = fields.Boolean(
                    "With PO",)
                    
    purchase_orders_ids = fields.One2many(
        'purchase.order.line',
        'order_id',
        string='Purchase Orders'
    )

    def action_create_po(self):
        self.ensure_one()
        purchase_order_obj = self.env['purchase.order']
        purchase_order_line_obj = self.env['purchase.order.line']

     
        po = purchase_order_obj.create({
            'partner_id': self.request_vendor.id,
            'origin': self.name,
            'date_order': fields.Date.today(),
        })

        for line in self.order_line:
            purchase_order_line_obj.create({
                'order_id': po.id,
                'name': line.name,
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'date_planned': fields.Date.today(),
            })

        return True
    def action_confirm(self):
        if self.no_kontrak:
            existing_contracts = self.search([('no_kontrak', '=', self.no_kontrak),
                                              ('id', '!=', self.id),
                                              ('state', '!=', 'cancel')])
            if existing_contracts:
                raise UserError(_("No Kontrak sudah pernah diinputkan sebelumnya...!"))
        return super(SaleOrder, self).action_confirm()

    def action_import_so_lines(self):
        return {
            'name': 'Import SO Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'import.so.lines.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }