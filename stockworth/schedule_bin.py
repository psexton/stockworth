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
from interval import Interval


class ScheduleBin:
    """
    For a given Equity, the "bin" that should be used for the VestingSchedule

    Implements hashable and sortable.
    """

    already_vested = date.fromisoformat("2000-01-01")  # flag date for "already vested"

    def __init__(self, equity, interval):
        self.equity = equity
        self.interval = interval
        self.key = self.compute_key()

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key

    # Key used for sorting and hashing (e.g. as the key in a dict)
    def compute_key(self):
        equity_date = self.equity.date
        if equity_date <= date.today():
            return self.already_vested
        else:
            if self.interval is Interval.MONTHLY:
                return equity_date.replace(day=1)
            else:
                return equity_date.replace(day=1, month=1)

    # Formatted string version
    def __repr__(self):
        # Replace the flag date with "Vested"
        if self.key == self.already_vested:
            return "Vested"
        else:
            if self.interval is Interval.MONTHLY:
                return self.key.strftime("%b %Y")
            else:
                return self.key.strftime("%Y")
