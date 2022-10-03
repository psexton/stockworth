# stockworth

Prints out an inspirational message telling you just how large your golden handcuffs are. The script only works for a single stock, and isn't smart enough to figure out vesting schedules. You need to enter in every payout. It does handle both RSUs and NSOs though.

Inspired by [JWZ's worth.pl script](https://www.jwz.org/hacks/).


## Setup

```
$ export ALPHAVANTAGE_API_KEY=XXXXXXXX
$ pip install -r requirements.txt
```

Stock prices are pulled from [Alpha Vantage](https://www.alphavantage.co/), using the [RomelTorres/alpha_vantage](https://github.com/RomelTorres/alpha_vantage) library. You'll need a free API key that you can get [here](https://www.alphavantage.co/support/#api-key).

You'll also need to provide a json config file containing the ticker symbol, your grant info, and your buckets for how much is okay to leave behind. An example can be found in [example_config.json](example_config.json).

If you prefer, you can supply the apikey as a `"apikey":"XXXXXXXX"` object in your config file instead of as an env var.

## Running

```
$ ./stockworth/stockworth.py --file example_config.json
GME is trading at 164.50. Your total equity is worth $997,414.
If you quit today, you will be walking away from $787,490.
Only 0 years, 11 months, and 28 days until that's less than $500,000.
Only 2 years, 0 months, and 29 days until that's less than $100,000.
Hang in there!
```

You can also pass in the stock price, useful for evaulating different future price scenarios.

```
$  ./stockworth/stockworth.py --file example_config.json --price 500
GME last closed at 500.00. At that price, your total equity is worth $3,081,574.
<!---SNIP--->
```

If you want to see the valuation post-tax instead of pre-tax, you can specify that either as a config file entry or as an arg at runtime.
```
{
    "tax_rate": 0.25
}
```

```
./stockworth/stockworth.py --tax-rate 0.25
```

## Testing

```
$ python -m unittest
```

## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
