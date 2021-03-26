from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)

        # Autoconfirm
        res.action_confirm()

        return res