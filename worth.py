#!/usr/bin/env python

import json
import os
from alpha_vantage.timeseries import TimeSeries


def main():
    # read in config file
    with open('config.json', 'r') as config_file:
        config = json.loads(config_file.read())

    # look up current price
    ticker_symbol = config["symbol"]
    latest_price = get_latest_price(ticker_symbol)
    print(f"stock={ticker_symbol}, latest_price={latest_price:,.2f}")

    # convert RSUs into date/value pairs
    # convert options into date/value pairs
    # compute total value

    # split out unvested equity from vested

    # sort unvested values by date
    # for each date, subtract amount that vests on that date
    # for each threshold, check if remaining amount is less
    # iterate until we run out of thresholds or we run out of equity
    # produce threshold/date pairs

    # for each threshold date, compute duration from now

    # pretty print


# Use the "quote endpoint" from alphavantage
# <https://www.alphavantage.co/documentation/#latestprice>
def get_latest_price(ticker_symbol):
    ts = TimeSeries(key=os.environ["ALPHAVANTAGE_API_KEY"])
    data, meta_data = ts.get_quote_endpoint(ticker_symbol)
    latest_price = float(data["05. price"])
    return latest_price


if __name__ == "__main__":
    main()
