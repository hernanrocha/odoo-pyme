# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    categ_id = fields.Many2one('product.category', related='product_id.categ_id', store=True)
