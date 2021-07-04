#!/usr/bin/env python

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

import argparse
import json
import os
from alpha_vantage.timeseries import TimeSeries
from datetime import date
from dateutil.relativedelta import relativedelta

from equity import Equity
from equity_group import EquityGroup
from threshold import Threshold
from vesting_schedule import VestingSchedule


def main():
    # read in config file
    config = read_config()

    # look up current price
    ticker_symbol = config["symbol"]
    latest_price = get_latest_price(ticker_symbol, config["apikey"])
    # print(f"stock={ticker_symbol}, latest_price={latest_price:,.2f}")

    # convert RSUs and options into date/value pairs
    all_equity = convert_to_equity(latest_price, config)

    # compute total value
    total_value = all_equity.total_value()
    # print(f"total_value={format_currency(total_value)}")

    # split out unvested equity from vested
    vested_value = all_equity.vested_value()
    unvested_value = total_value - vested_value
    # print(f"vested_value={format_currency(vested_value)}")

    # produce threshold/date pairs
    thresholds = compute_thresholds(threshold_values=config["thresholds"], equity=all_equity)
    # print(f"thresholds={thresholds}")

    # pretty print
    message = f"{ticker_symbol} last closed at {latest_price:,.2f}. " \
              f"At that price, your total equity is worth {format_currency(total_value)}." \
              f"\nYour vesting schedule is"
    for entry in compute_and_format_vesting_schedule(all_equity):
        message += f"\n\t{entry}"
    message += f"\nIf you quit today, you will be walking away from {format_currency(unvested_value)}."
    for threshold in thresholds:
        message += f"\n\tOnly {format_date_delta(threshold.date)} until that's less than {format_currency(threshold.amount)}."
    message += "\nHang in there!"
    print(message)


def read_config():
    # read in config file name
    parser = argparse.ArgumentParser(prog="stockworth.py")
    parser.add_argument("-f", "--file", default="config.json",
                        help="The json file to read the config from (defaults to config.json).")
    args = parser.parse_args()

    with open(args.file, 'r') as config_file:
        config = json.loads(config_file.read())

    # if config did not contain apikey, try to read it from env var
    if not "apikey" in config:
        env_api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if env_api_key is None:
            raise Exception("Could not find api key")
        else:
            config["apikey"] = env_api_key

    return config


# Use the "quote endpoint" from alphavantage
# <https://www.alphavantage.co/documentation/#latestprice>
def get_latest_price(ticker_symbol, api_key):
    ts = TimeSeries(key=api_key)
    data, meta_data = ts.get_quote_endpoint(ticker_symbol)
    latest_price = float(data["05. price"])
    return latest_price


def convert_to_equity(latest_price, config):
    # convert rsus into date/value pairs
    rsus = list(map(
        lambda rsu: Equity.from_rsu(
            current_price=latest_price,
            quantity=rsu["qty"],
            vest_date=rsu["vest_date"]
        ),
        config["rsus"]
    ))
    # print(f"rsus={rsus}")

    # convert options into date/value pairs
    options = list(map(
        lambda option: Equity.from_option(
            current_price=latest_price,
            quantity=option["qty"],
            vest_date=option["vest_date"],
            strike_price=option["price"]
        ),
        config["options"]
    ))
    # print(f"options={options}")

    return EquityGroup(rsus + options)


def compute_thresholds(threshold_values, equity):
    thresholds = list(map(lambda threshold: Threshold(threshold, equity), threshold_values))
    return thresholds


def compute_and_format_vesting_schedule(all_equity):
    # produce vesting schedule
    schedule = VestingSchedule(all_equity)
    # sort the dictionary,
    # and replace the flag date with "Vested"
    formatted_lines = []
    for key, value in sorted(schedule.vesting_months.items()):
        formatted_key = "Vested" if key == schedule.already_vested else key.strftime("%b %Y")
        formatted_value = format_currency(value)
        formatted_lines.append(f"{formatted_key}: {formatted_value}")
    return formatted_lines


def format_currency(amount):
    # prefix with $, separate at thousands with ',', no decimal places
    return f"${amount:,.0f}"


def format_date_delta(future_date):
    start_date = date.today()
    diff = relativedelta(future_date, start_date)
    return f"{diff.years} years, {diff.months} months, and {diff.days} days"


if __name__ == "__main__":
    main()
