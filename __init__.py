# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import stock


def register():
    Pool.register(
        stock.Lot,
        module='stock_lot_jreport', type_='model')
    Pool.register(
        stock.LotReport,
        module='stock_lot_jreport', type_='report')
