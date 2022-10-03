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

from threshold import Threshold


class EquityGroup:
    """ Models a RSU or NSO grant with multiple vesting dates """

    def __init__(self, equity_list):
        self.equity_list = equity_list
        self.vesting_dates = set(e.date for e in equity_list)

    def total_value(self):
        """ The value after all equities in the group have vested """
        return sum(e.value for e in self.equity_list)

    def vested_value(self):
        """ The value of the group today """
        return self.value_at(date.today())

    def value_at(self, target_date):
        """ The value of the group at a given date """
        return sum(e.value_at(target_date) for e in self.equity_list)

    def compute_thresholds(self, amounts):
        return list(map(lambda amount: self.compute_threshold(amount), amounts))

    def compute_threshold(self, amount):
        """
        Compute a threshold for this equity group
        For an amount X, the threshold date is when this group's unvested equity will be less than X.
        """
        # We don't expect to have more than 10s of entries, so a linear search is fine
        # Iterate through all vesting dates in ascending order, until we find one where
        # the unvested value is less than the threshold amount.
        # All equity vests _eventually_, at which point unvested will be 0,
        # so we're guaranteed to find an answer.

        sorted_vesting_dates = sorted(self.vesting_dates)
        for vesting_date in sorted_vesting_dates:
            vested_at_threshold = self.total_value() - amount
            if self.value_at(vesting_date) >= vested_at_threshold:
                return Threshold(amount, vesting_date)
