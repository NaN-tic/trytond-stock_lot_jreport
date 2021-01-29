# This file is part of stock_lot_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.modules.jasper_reports.jasper import JasperReport
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from dateutil.relativedelta import relativedelta

__all__ = ['LotReport']


class LotReport(JasperReport):
    __name__ = 'stock.lot.jreport'
