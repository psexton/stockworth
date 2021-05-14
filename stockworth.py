#!/usr/bin/env python

import argparse
import json
import os
from alpha_vantage.timeseries import TimeSeries
from datetime import date
from dateutil.relativedelta import relativedelta

from equity import Equity
from equity_group import EquityGroup
from threshold import Threshold


def main():
    # read in config file
    config = read_config()

    # look up current price
    ticker_symbol = config["symbol"]
    latest_price = get_latest_price(ticker_symbol)
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
    message = f"{ticker_symbol} is trading at {latest_price:,.2f}. " \
              f"Your total equity is worth {format_currency(total_value)}. " \
              f"If you quit today, you will be walking away from {format_currency(unvested_value)}."
    for threshold in thresholds:
        message += f"\nOnly {format_date_delta(threshold.date)} until that's less than {format_currency(threshold.amount)}."
    message += "\nHang in there!"
    print(message)


def read_config():
    # read in config file name
    parser = argparse.ArgumentParser(prog="stockworth.py")
    parser.add_argument("-f", "--file", default="config.json",
                        help="The json file to read the config from (defaults to config.json).")
    args = parser.parse_args()

    with open(args.file, 'r') as config_file:
        return json.loads(config_file.read())


# Use the "quote endpoint" from alphavantage
# <https://www.alphavantage.co/documentation/#latestprice>
def get_latest_price(ticker_symbol):
    ts = TimeSeries(key=os.environ["ALPHAVANTAGE_API_KEY"])
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


def format_currency(amount):
    # prefix with $, separate at thousands with ',', no decimal places
    return f"${amount:,.0f}"


def format_date_delta(future_date):
    start_date = date.today()
    diff = relativedelta(future_date, start_date)
    return f"{diff.years} years, {diff.months} months, and {diff.days} days"


if __name__ == "__main__":
    main()
