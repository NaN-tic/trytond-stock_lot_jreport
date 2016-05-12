# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .stock import *


def register():
    Pool.register(
        Lot,
        module='stock_lot_jreport', type_='model')
    Pool.register(
        LotReport,
        module='stock_lot_jreport', type_='report')
