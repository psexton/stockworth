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

from datetime import date


class Threshold:
    def __init__(self, amount, equity_group):
        self.amount = amount
        self.equity_group = equity_group
        self.date = self._compute_date()

    def __repr__(self):
        return f"({self.amount} -> {self.date})"

    def _compute_date(self):
        # Need to compute when unvested equity will be less than the threshold amount
        # Subtract the threshold from the total equity value
        total_equity_value = self.equity_group.total_value()
        vested_at_threshold = total_equity_value - self.amount
        # Now iterate over equity vest dates, in ascending order,
        # until that value is >= the subtraction result
        vesting_dates = sorted(self.equity_group.vesting_dates)
        for vesting_date in vesting_dates:
            if self.equity_group.value_at(vesting_date) >= vested_at_threshold:
                return vesting_date
