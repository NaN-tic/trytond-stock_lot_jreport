#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction


class TestCase(unittest.TestCase):
    'Test module'

    def setUp(self):
        trytond.tests.test_tryton.install_module(
            'stock_lot_jreport')
        self.company = POOL.get('company.company')
        self.user = POOL.get('res.user')
        self.stock_configuration = POOL.get('stock.configuration')
        self.uom = POOL.get('product.uom')
        self.template = POOL.get('product.template')
        self.product = POOL.get('product.product')
        self.location = POOL.get('stock.location')
        self.move = POOL.get('stock.move')
        self.lot = POOL.get('stock.lot')

    def test0005views(self):
        'Test views'
        test_view('stock_lot_jreport')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010get_lag_quantity(self):
        'Test get_lag_quantity'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):

            supplier, = self.location.search([('code', '=', 'SUP')])
            customer, = self.location.search([('code', '=', 'CUS')])
            storage, = self.location.search([('code', '=', 'STO')])
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])
            currency = company.currency
            self.user.write([self.user(USER)], {
                'main_company': company.id,
                'company': company.id,
                })
            self.stock_configuration.create([{
                    'warehouse': storage.id,
                    'lag_days': 1,
                    }])

            unit, = self.uom.search([('name', '=', 'Unit')])
            template, = self.template.create([{
                        'name': 'Test period',
                        'type': 'goods',
                        'cost_price_method': 'fixed',
                        'default_uom': unit.id,
                        'list_price': Decimal(0),
                        'cost_price': Decimal(0),
                        }])
            product, = self.product.create([{
                        'template': template.id,
                        }])

            lot1, lot2 = self.lot.create([{
                        'number': '1',
                        'product': product.id,
                        }, {
                        'number': '2',
                        'product': product.id,
                        }])

            today = datetime.date.today()
            moves = self.move.create([{
                        'product': product.id,
                        'lot': lot1.id,
                        'uom': unit.id,
                        'quantity': 5,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 10,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 2,
                        'from_location': storage.id,
                        'to_location': customer.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'lot': lot1.id,
                        'uom': unit.id,
                        'quantity': 5,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'planned_date': today + relativedelta(days=2),
                        'effective_date': today + relativedelta(days=2),
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 10,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'planned_date': today - relativedelta(days=1),
                        'effective_date': today - relativedelta(days=1),
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }])
            self.move.do(moves)

            quantities = {
                '1': 5,
                '2': 18,
                }

            lots = self.lot.search([])
            for lot in lots:
                self.assertEqual(lot.lag_quantity, quantities[lot.number])


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
