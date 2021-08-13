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
    """
    A threshold is a milestone for future vesting

    It answers the question of "How long do I have to stay to leave less than X on the table"
    Given an EquityGroup, and an amount, it computes the date on which the group's unvested
    equity is less than that amount.
    """

    def __init__(self, amount, equity_group):
        self.amount = amount
        self.equity_group = equity_group
        self.date = self._compute_date()

    def __repr__(self):
        return f"({self.amount} -> {self.date})"

    def _compute_date(self):
        # We don't expect to have more than 10s of entries, so a linear search is fine
        # Iterate through all vesting dates in ascending order, until we find one where
        # the unvested value is less than the threshold amount.
        # All equity vests _eventually_, at which point unvested will be 0,
        # so we're guaranteed to find an answer.

        total_equity_value = self.equity_group.total_value()
        vested_at_threshold = total_equity_value - self.amount
        
        vesting_dates = sorted(self.equity_group.vesting_dates)
        for vesting_date in vesting_dates:
            if self.equity_group.value_at(vesting_date) >= vested_at_threshold:
                return vesting_date
