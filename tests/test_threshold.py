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
from stockworth.threshold import Threshold


class TestThreshold(unittest.TestCase):
    def setUp(self):
        today = date.today()
        self.last_month = [
            Equity(today - timedelta(days=40), 100.0),
            Equity(today - timedelta(days=42), 100.0),
            Equity(today - timedelta(days=44), 100.0),
        ]
        self.last_month_value = 300
        self.next_month = [
            Equity(today + timedelta(days=46), 10.0),
            Equity(today + timedelta(days=48), 10.0),
        ]
        self.next_month_value = 20
        self.next_year = [Equity(today + timedelta(days=365), 1.0)]
        self.next_year_value = 1
        self.instance = EquityGroup(self.last_month + self.next_month + self.next_year)

    def test_normal_path(self):
        # To leave no more than 15.0 unvested, one of next_month needs to vest
        amount = 15.0
        exp_result = Threshold(amount, self.next_month[0].date)
        result = self.instance.compute_threshold(amount)
        self.assertEqual(result, exp_result)

    def test_threshold_0(self):
        # To leave nothing unvested, everything needs to vest
        amount = 0.0
        exp_result = Threshold(amount, self.next_year[0].date)
        result = self.instance.compute_threshold(amount)
        self.assertEqual(result, exp_result)


if __name__ == "__main__":
    unittest.main()
