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

from collections import namedtuple

""" 
A threshold is a milestone for future vesting

    It answers the question of "How long do I have to stay to leave less than X on the table"
    Given an EquityGroup, and an amount, it computes the date on which the group's unvested
    equity is less than that amount.

    Thresholds are created using the `compute_threshold(s)` methods of an EquityGroup.
"""
Threshold = namedtuple("Threshold", ["amount", "date"])
