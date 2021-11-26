# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models
import datetime

class MonthlyResultsReportLine(models.Model):
    _name = "monthly.results.report.line"

    name = fields.Char(string="Categoria")
    purchases = fields.Float(string='Total Compras')
    sales = fields.Float(string='Total Ventas')
    start_stock = fields.Float(string='Inventario Inicial')
    end_stock = fields.Float(string='Inventario Final')
    net = fields.Float(string="Resultado")

    report_id = fields.Many2one(comodel_name="monthly.results.report", 
        ondelete="cascade", invisible=True)

class MonthlyResultsReport(models.Model):
    _name = "monthly.results.report"

    name = fields.Char(string="Nombre")
    start_date = fields.Datetime(string='Fecha Desde')
    end_date = fields.Datetime(string='Fecha Hasta')

    line_ids = fields.One2many(
        comodel_name='monthly.results.report.line',
        inverse_name='report_id',
        string="Lineas")

    sale_ids = fields.Many2many(
        comodel_name='sale.order',
        # check_company=True)
        string="Ventas")

    purchase_ids = fields.Many2many(
        comodel_name='purchase.order',
        # check_company=True)
        string="Compras")

    purchases_total = fields.Float(string='Total Compras')
    sales_total = fields.Float(string='Total Ventas')
    start_stock = fields.Float(string='Inventario Inicial')
    end_stock = fields.Float(string='Inventario Final')

    def compute_results(self):
        # Compras
        self.purchase_ids = self.env['purchase.order'].search([
            ('date_approve', '>=', self.start_date),
            ('date_approve', '<', self.end_date)]
        )
        self.purchases_total = sum(self.purchase_ids.mapped('amount_total'))

        # Ventas
        self.sale_ids = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<', self.end_date)]
        )
        self.sales_total = sum(self.sale_ids.mapped('amount_total'))

        inv_inicial = self.env['stock.valuation.layer'].read_group([
            ('product_id.type','=','product'),
            ('create_date', '<=', self.start_date)
        ], ['quantity:sum', 'value:sum'], ['categ_id'], lazy=False)
        self.start_stock = sum(list(map(lambda r: r['value'], inv_inicial)))

        inv_final = self.env['stock.valuation.layer'].read_group([
            ('product_id.type','=','product'),
            ('create_date', '<=', self.end_date)
        ], ['quantity:sum', 'value:sum'], ['categ_id'], lazy=False)
        self.end_stock = sum(list(map(lambda r: r['value'], inv_final)))

        self.line_ids = [(5,0,0)]
        categ_ids = self.env['product.category'].search([])

        p_ids = self.purchase_ids.mapped('order_line')
        s_ids = self.sale_ids.mapped('order_line')

        for categ_id in categ_ids:
            filtered_purchases = p_ids.filtered(
                lambda l: l.product_id.categ_id.id == categ_id.id)
            purchases_i = sum(filtered_purchases.mapped('price_subtotal'))

            filtered_sales = s_ids.filtered(
                lambda l: l.product_id.categ_id.id == categ_id.id)
            sales_i = sum(filtered_sales.mapped('price_subtotal'))

            # 'categ_id' es una tupla de 2 elementos: id y puntero a category
            inicial_i = list(filter(lambda l: l['categ_id'][0] == categ_id.id, inv_inicial))
            inicial_i = inicial_i[0]['value'] if inicial_i else 0

            # 'categ_id' es una tupla de 2 elementos: id y puntero a category
            final_i = list(filter(lambda l: l['categ_id'][0] == categ_id.id, inv_final))
            final_i = final_i[0]['value'] if final_i else 0

            cmv_i = inicial_i + purchases_i - final_i
            net_i = sales_i - cmv_i

            self.line_ids.create({
                'name': categ_id.name,
                'purchases': purchases_i,
                'sales': sales_i,
                'start_stock': inicial_i,
                'end_stock': final_i,
                'net': net_i,
                'report_id': self.id
            })

    @api.depends('purchases_total', 'sales_total', 'start_stock', 'end_stock')
    def _compute_net_total(self):
        for r in self:
            cmv = r.start_stock + r.purchases_total - r.end_stock
            r.net_total = r.sales_total - cmv

    net_total = fields.Float(string='Resultado Neto', compute=_compute_net_total)