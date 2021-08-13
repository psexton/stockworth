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

import locale
from datetime import date


class Equity:
    """
    Represents a piece of equity

    This is not very useful by itself, but is used to build a EquityGroup,
    which can model a RSU or NSO grant with multiple vesting dates.
    """

    # Accept either a date object or an ISO8601 date string
    def __init__(self, vest_date, value):
        self.date = vest_date if isinstance(vest_date, date) else date.fromisoformat(vest_date)
        self.value = value

    def __repr__(self):
        return f"({self.date} -> {locale.currency(self.value)})"

    def value_at(self, target_date):
        """ The value of the equity at a given date """
        return self.value if target_date >= self.date else 0.0

    @staticmethod
    def from_rsu(current_price, quantity, vest_date):
        value = current_price * quantity
        return Equity(vest_date, value)

    @staticmethod
    def from_option(current_price, quantity, vest_date, strike_price):
        purchase_price = quantity * strike_price
        sale_price = current_price * quantity
        value = max(sale_price - purchase_price, 0.0)  # options have a minimum value of worthless
        return Equity(vest_date, value)
