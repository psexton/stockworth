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
from stockworth.equity_group import EquityGroup


class TestEquityGroup(unittest.TestCase):

    def setUp(self):
        today = date.today()
        self.last_month = [
            Equity(today - timedelta(days=40), 100.0),
            Equity(today - timedelta(days=42), 100.0),
            Equity(today - timedelta(days=44), 100.0)
        ]
        self.last_month_value = 300
        self.next_month = [
            Equity(today + timedelta(days=46), 10.0),
            Equity(today + timedelta(days=48), 10.0)
        ]
        self.next_month_value = 20
        self.next_year = [Equity(today + timedelta(days=365), 1.0)]
        self.next_year_value = 1
        self.instance = EquityGroup(self.last_month + self.next_month + self.next_year)

    def test_total_value_empty(self):
        instance = EquityGroup([])
        self.assertEqual(instance.total_value(), 0.0)

    def test_total_value_single(self):
        single_equity = self.last_month[0]
        instance = EquityGroup([single_equity])
        self.assertEqual(instance.total_value(), single_equity.value)

    def test_total_value_group(self):
        instance = EquityGroup(self.last_month)
        self.assertEqual(instance.total_value(), self.last_month_value)

    def test_vested_value(self):
        instance = EquityGroup(self.last_month + self.next_month + self.next_year)
        result = instance.vested_value()
        exp_result = self.last_month_value
        self.assertEqual(result, exp_result)

    def test_value_at_today(self):
        instance = EquityGroup(self.last_month + self.next_month + self.next_year)
        result = instance.value_at(date.today())
        exp_result = self.last_month_value
        self.assertEqual(result, exp_result)

    def test_value_at_past(self):
        instance = EquityGroup(self.last_month + self.next_month + self.next_year)
        result = instance.value_at(date.today() - timedelta(weeks=8))
        exp_result = 0
        self.assertEqual(result, exp_result)

    def test_value_at_future(self):
        instance = EquityGroup(self.last_month + self.next_month + self.next_year)
        result = instance.value_at(date.today() + timedelta(weeks=8))
        exp_result = self.last_month_value + self.next_month_value
        self.assertEqual(result, exp_result)

    def test_value_at_far_future(self):
        instance = EquityGroup(self.last_month + self.next_month + self.next_year)
        result = instance.value_at(date.today() + timedelta(weeks=100))
        exp_result = self.last_month_value + self.next_month_value + self.next_year_value
        self.assertEqual(result, exp_result)


if __name__ == '__main__':
    unittest.main()
