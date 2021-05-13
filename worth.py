#!/usr/bin/env python

import json
import locale
import os
from alpha_vantage.timeseries import TimeSeries

from equity import Equity
from equity_group import EquityGroup
from threshold import Threshold


def main():
    # read in config file
    with open('config.json', 'r') as config_file:
        config = json.loads(config_file.read())

    # look up current price
    ticker_symbol = config["symbol"]
    latest_price = get_latest_price(ticker_symbol)
    print(f"stock={ticker_symbol}, latest_price={latest_price:,.2f}")

    # convert RSUs and options into date/value pairs
    all_equity = convert_to_equity(latest_price, config)

    # compute total value
    total_value = all_equity.total_value()
    print(f"total_value={locale.currency(total_value)}")

    # split out unvested equity from vested
    vested_value = all_equity.vested_value()
    print(f"vested_value={locale.currency(vested_value)}")

    # produce threshold/date pairs
    thresholds = compute_thresholds(threshold_values=config["thresholds"], equity=all_equity)
    

    # pretty print


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
    # print(f"thresholds={thresholds}")
    return thresholds


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    main()
