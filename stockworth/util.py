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
from dateutil.relativedelta import relativedelta


def format_currency(amount):
    # prefix with $, separate at thousands with ',', no decimal places
    return f"${amount:,.0f}"


def format_date_delta(future_date):
    start_date = date.today()
    diff = relativedelta(future_date, start_date)
    return f"{diff.years} years, {diff.months} months, and {diff.days} days"
