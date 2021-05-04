from odoo import api, models, fields
from datetime import date

# Cantidad Fisica / Proyectada
# Informacion de ganancia por venta estimada (de la mercaderia existente)
# Mostrar dashboard de entregas pendientes para el dia de hoy (armar dashboard inicial)
# Tablet de acceso mobile para tener mas resolucion de pantalla
#  - Internet desde el celular
#  - Bateria cargada desde el auto (o power bank)

class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def _default_name(self):
        return "Inventario {}".format(date.today().strftime('%d/%m/%Y'))

    name = fields.Char(default=lambda self: self._default_name(), readonly=False)
    exhausted = fields.Boolean(default=True)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # TODO: Configurar valores por defecto desde UI
    def _default_partner_id(self):
        default_partner = self.env['res.partner'].search([('name', 'like', 'Consumidor Final')])
        if len(default_partner) == 0:
            return None
        return default_partner.id

    # TODO: Averiguar por que se este no se traduce 
    def _default_payment_term_id(self):
        default_payment_term = self.env['account.payment.term'].search([])
        if len(default_payment_term) == 0:
            return None
        return default_payment_term[0].id

    partner_id = fields.Many2one(default=lambda self: self._default_partner_id())
    payment_term_id = fields.Many2one(default=lambda self: self._default_payment_term_id())

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)

        # Autoconfirm (state=sale, date_order=today())
        res.action_confirm()
        
        return res

    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        for order in self:

            # TODO: add ["is_delivery_set_to_done", "create_invoice", "validate_invoice"] to settings
            # taken from sale_order_automation modules

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

            # Move Sale Order to Done
            order.action_done()

        return res 

# @api.onchange('product_id')
# def onchange_product_id(self):
#     self.price_unit = self.product_id.standard_price or 0.0