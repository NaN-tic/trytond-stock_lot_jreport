# This file is part of stock_lot_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.modules.jasper_reports.jasper import JasperReport


class LotReport(JasperReport):
    __name__ = 'stock.lot.jreport'
