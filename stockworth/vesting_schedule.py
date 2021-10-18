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

from schedule_bin import ScheduleBin
from util import format_currency


# Given a EquityGroup, bin the value by vesting month.
# Put everything already vested in a single bin.

class VestingSchedule:
    def __init__(self, equity_group, bin_size):
        self.equity_group = equity_group
        self.vesting_bins = self._compute_schedule(bin_size)

    def _compute_schedule(self, bin_size):
        output = {}
        for equity in self.equity_group.equity_list:
            key = ScheduleBin(equity, bin_size)
            if key in output:
                output[key] = output[key] + equity.value
            else:
                output[key] = equity.value
        return output

    def compute_and_format_schedule(self):
        # sort the dictionary,
        formatted_lines = []
        for key, value in sorted(self.vesting_bins.items()):
            formatted_value = format_currency(value)
            formatted_lines.append(f"{key}: {formatted_value}")
        return formatted_lines
