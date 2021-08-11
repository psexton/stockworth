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
    def __init__(self, date_str, value):
        self.date = date.fromisoformat(date_str)
        self.value = value

    def __repr__(self):
        return f"({self.date} -> {locale.currency(self.value)})"

    def is_vested_by(self, target_date):
        return self.date <= target_date

    @staticmethod
    def from_rsu(current_price, quantity, vest_date):
        value = current_price * quantity
        return Equity(vest_date, value)

    @staticmethod
    def from_option(current_price, quantity, vest_date, strike_price):
        purchase_price = quantity * strike_price
        sale_price = current_price * quantity
        value = sale_price - purchase_price
        return Equity(vest_date, value)
