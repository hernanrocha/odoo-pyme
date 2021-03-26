from odoo import models, api, fields, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(default='product')
