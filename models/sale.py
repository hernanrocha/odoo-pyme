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

        # Autoconfirm
        res.action_confirm()

        return res


# @api.onchange('product_id')
# def onchange_product_id(self):
#     self.price_unit = self.product_id.standard_price or 0.0