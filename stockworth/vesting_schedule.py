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
from util import format_currency


# Given a EquityGroup, bin the value by vesting month.
# Put everything already vested in a single bin.

class VestingSchedule:
    def __init__(self, equity_group):
        self.equity_group = equity_group
        self.already_vested = date.fromisoformat('2000-01-01')  # flag date for "already vested"
        self.vesting_months = self._compute_schedule()

    def _compute_schedule(self):
        vested_key = self.already_vested
        output = {}
        for equity in self.equity_group.equity_list:
            if equity.date <= date.today():
                if vested_key in output:
                    output[vested_key] = output[vested_key] + equity.value
                else:
                    output[vested_key] = equity.value
            else:
                month = equity.date.replace(day=1)
                if month in output:
                    output[month] = output[month] + equity.value
                else:
                    output[month] = equity.value
        return output

    def compute_and_format_schedule(self):
        # sort the dictionary,
        # and replace the flag date with "Vested"
        formatted_lines = []
        for key, value in sorted(self.vesting_months.items()):
            formatted_key = "Vested" if key == self.already_vested else key.strftime("%b %Y")
            formatted_value = format_currency(value)
            formatted_lines.append(f"{formatted_key}: {formatted_value}")
        return formatted_lines
