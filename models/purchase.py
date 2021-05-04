from odoo import api, models, fields
from odoo.exceptions import ValidationError

# Valid states: draft, purchase, done, cancel
# Transiciones: 
#  - New:                   -> draft
#  - Save:         draft    -> purchase
#  - Cancel        purchase -> cancel
#  - Mark As Done: purchase -> done
#  - To Draft      cancel   -> draft

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)

        # Autoconfirm
        res.button_confirm()

        return res

    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        for order in self:

            # warehouse = order.warehouse_id
            # if warehouse.is_delivery_set_to_done and order.picking_ids: 
            for picking in order.picking_ids:
                picking.action_assign()
                picking.action_confirm()
                for mv in picking.move_ids_without_package:
                    mv.quantity_done = mv.product_uom_qty
                picking.button_validate()

            # if warehouse.create_invoice and not order.invoice_ids:
            #     order._create_invoices()  

            # if warehouse.validate_invoice and order.invoice_ids:
            #     for invoice in order.invoice_ids:
            #         invoice.action_post()

            # Move Purchase Order to Done
            order.button_done()

        return res