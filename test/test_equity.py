# <editor-fold desc="AGPLv3 preamble">
# stockworth, a simple equity pretty printer
# Copyright (C) 2021  Paul Sexton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# </editor-fold>

import unittest
from datetime import date, timedelta

from stockworth.equity import Equity


class TestEquity(unittest.TestCase):

    def test_value_at_today(self):
        instance = Equity(date.today(), 100.0)
        result = instance.value_at(date.today())
        exp_result = instance.value
        self.assertEqual(result, exp_result)

    def test_value_at_past(self):
        instance = Equity(date.today(), 100.0)
        result = instance.value_at(date.today() - timedelta(days=1))
        exp_result = 0.0
        self.assertEqual(result, exp_result)

    def test_value_at_future(self):
        instance = Equity(date.today(), 100.0)
        result = instance.value_at(date.today() + timedelta(days=1))
        exp_result = instance.value
        self.assertEqual(result, exp_result)

    # Happy path test
    def test_from_rsu(self):
        vest_date = date(2020, 7, 8)
        shares = 5.0
        price = 12.5
        exp_value = shares * price
        instance = Equity.from_rsu(price, shares, vest_date.isoformat())

        self.assertEqual(instance.date, vest_date)
        self.assertEqual(instance.value, exp_value)

    # Happy path test
    def test_from_option(self):
        vest_date = date(2021, 2, 3)
        shares = 5.0
        current_price = 15.0
        strike_price = 14.0
        exp_value = (current_price - strike_price) * shares
        instance = Equity.from_option(current_price, shares, vest_date.isoformat(), strike_price)

        self.assertEqual(instance.date, vest_date)
        self.assertEqual(instance.value, exp_value)

    # Options can be worthless but they can't cost you money
    def test_from_option_underwater(self):
        shares = 5.0
        current_price = 10.0
        strike_price = 14.0
        exp_value = 0.0
        instance = Equity.from_option(current_price, shares, date.today().isoformat(), strike_price)

        self.assertEqual(instance.value, exp_value)

    # Edge case of current price being exactly the strike price
    def test_from_option_precisely_worthless(self):
        shares = 5.0
        current_price = 10.0
        strike_price = 10.0
        exp_value = 0.0
        instance = Equity.from_option(current_price, shares, date.today().isoformat(), strike_price)

        self.assertEqual(instance.value, exp_value)


if __name__ == '__main__':
    unittest.main()
