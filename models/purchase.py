from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)

        # Autoconfirm
        res.button_confirm()
        
        return res
