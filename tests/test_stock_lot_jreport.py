#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction

from trytond.modules.company.tests import create_company, set_company


class TestCase(ModuleTestCase):
    'Test module'
    module = 'stock_lot_jreport'

    @with_transaction()
    def test0010get_lag_quantity(self):
        'Test get_lag_quantity'
        pool = Pool()
        StockConfiguration = pool.get('stock.configuration')
        Uom = pool.get('product.uom')
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Location = pool.get('stock.location')
        Move = pool.get('stock.move')
        Lot = pool.get('stock.lot')

        # Create Company
        company = create_company()
        with set_company(company):

            supplier, = Location.search([('code', '=', 'SUP')])
            customer, = Location.search([('code', '=', 'CUS')])
            storage, = Location.search([('code', '=', 'STO')])
            warehouse, = Location.search([('code', '=', 'WH')])

            StockConfiguration.create([{
                    'warehouse': warehouse.id,
                    'lag_days': 1,
                    }])

            unit, = Uom.search([('name', '=', 'Unit')])
            template, = Template.create([{
                        'name': 'Test period',
                        'type': 'goods',
                        'cost_price_method': 'fixed',
                        'default_uom': unit.id,
                        'list_price': Decimal(0),
                        }])
            product, = Product.create([{
                        'template': template.id,
                        }])

            lot1, lot2 = Lot.create([{
                        'number': '1',
                        'product': product.id,
                        }, {
                        'number': '2',
                        'product': product.id,
                        }])

            today = datetime.date.today()
            moves = Move.create([{
                        'product': product.id,
                        'lot': lot1.id,
                        'uom': unit.id,
                        'quantity': 5,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'unit_price': Decimal('1'),
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 10,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'unit_price': Decimal('1'),
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 2,
                        'from_location': storage.id,
                        'to_location': customer.id,
                        'unit_price': Decimal('1'),
                        }, {
                        'product': product.id,
                        'lot': lot1.id,
                        'uom': unit.id,
                        'quantity': 5,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'planned_date': today + relativedelta(days=2),
                        'effective_date': today + relativedelta(days=2),
                        'unit_price': Decimal('1'),
                        }, {
                        'product': product.id,
                        'lot': lot2.id,
                        'uom': unit.id,
                        'quantity': 10,
                        'from_location': supplier.id,
                        'to_location': storage.id,
                        'planned_date': today - relativedelta(days=1),
                        'effective_date': today - relativedelta(days=1),
                        'unit_price': Decimal('1'),
                        }])
            Move.do(moves)

            quantities = {
                '1': 5,
                '2': 18,
                }

            lots = Lot.search([])
            for lot in lots:
                self.assertEqual(lot.lag_quantity, quantities[lot.number])


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
