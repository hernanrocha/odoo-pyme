from odoo import models, api, fields, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# product.template es el producto base
# product.supplierinfo es la informacion de los proveedores (almancena la lista de proveedores)
# product.product es una variante del producto. cada proveedor puede entregar una variante

# _order = 'sequence, min_qty desc, price'

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(default='product')

    seller_id = fields.Many2one(comodel_name="product.supplierinfo", string="Proveedor", 
        compute="_compute_seller_id", readonly=True)

    # TODO: add inverse method y sacar lista de proveedores
    seller_name = fields.Char(string="Proveedor", compute="_compute_seller_name", store=True)
    price_buy = fields.Float(string="Precio de Compra", compute="_compute_price_buy")

    @api.depends('seller_ids')
    def _compute_seller_id(self):
        for p in self:
            p.seller_id = p.seller_ids[:1].id

    @api.depends('seller_id')
    def _compute_price_buy(self):
        for p in self:
            p.price_buy = p.seller_id.price

    @api.depends('seller_id')
    def _compute_seller_name(self):
        for p in self:
            # seller_id.name is a res.partner reference
            p.seller_name = p.seller_id.name.display_name