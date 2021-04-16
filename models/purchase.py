from odoo import api, models, fields
from odoo.exceptions import ValidationError

# Valid states: draft, purchase, done, cancel
# Transiciones: 
#  - New:                   -> draft
#  - Save:         draft    -> purchase
#  - Cancel        purchase -> cancel
#  - Mark As Done: purchase -> done
#  - To Draft      cancel   -> draft

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _pre_action_done_hook(self):
        print("PRE ACTION DONE HOOK")
        return super(StockPicking, self)._pre_action_done_hook()

        # env['stock.immediate.transfer'].process()
        # return True

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)

        # Autoconfirm
        res.button_confirm()

        # Move to Done
        res.button_done()
        
        return res

    def action_done(self):
        for purchase in self:
            if purchase.state == 'purchase':
                # Confirmar Compra
                purchase.button_done()
            else:
                raise ValidationError("Solamente pueden marcarse como hechos los pedidos confirmados.")
        
        # TODO Marcar como hechas las ordenes de recepcion en inventario
        picking_list = self.env['stock.picking'].search([('origin', 'in', self.mapped('name'))])
        print(picking_list)

        # for picking in picking_list:
        #     print(picking)
        #     # stock_picking.py
        #     # TODO: no se marcan como recibidas
        #     v = picking.with_context(skip_immediate=True, skip_backorder=True).button_validate()
        #     print(v)
        #     transfer = self.env.ref('stock.view_immediate_transfer')
        #     print(transfer)
        #     print(transfer.process())