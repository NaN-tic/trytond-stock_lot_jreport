# This file is part of stock_lot_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.modules.jasper_reports.jasper import JasperReport
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

from dateutil.relativedelta import relativedelta


__all__ = ['Lot', 'LotReport']


class Lot:
    __metaclass__ = PoolMeta
    __name__ = 'stock.lot'

    lag_quantity = fields.Function(fields.Float('Lag Quantity'),
        'get_lag_quantity', searcher='search_lag_quantity')
    warehouse = fields.Function(fields.Many2One('stock.location',
            'Warehouse'), 'get_warehouse')

    @classmethod
    def get_lag_quantity(cls, lots, name):
        pool = Pool()
        Date = pool.get('ir.date')
        configuration = pool.get('stock.configuration')(1)

        products = list(set(l.product for l in lots))
        location_ids = (configuration.warehouse and
            [configuration.warehouse.id] or [])
        lag_days = configuration.lag_days or 0
        stock_date_end = Date.today() + relativedelta(days=int(lag_days))
        with Transaction().set_context({'stock_date_end': stock_date_end}):
            quantities = cls._get_quantity(lots, name, location_ids, products,
                grouping=('product', 'lot'))
            return quantities

    @classmethod
    def search_lag_quantity(cls, name, domain=None):
        pool = Pool()
        Date = pool.get('ir.date')
        configuration = pool.get('stock.configuration')(1)

        location_ids = (configuration.warehouse and
            [configuration.warehouse.id] or [])
        lag_days = configuration.lag_days or 0
        stock_date_end = Date.today() + relativedelta(days=int(lag_days))
        with Transaction().set_context({'stock_date_end': stock_date_end}):
            return cls._search_quantity(name, location_ids, domain,
                grouping=('product', 'lot'))

    @classmethod
    def get_warehouse(cls, lots, name):
        configuration = Pool().get('stock.configuration')(1)
        warehouse_id = (configuration.warehouse and
            configuration.warehouse.id or None)
        return {l.id: warehouse_id for l in lots}


class LotReport(JasperReport):
    __name__ = 'stock.lot.jreport'
