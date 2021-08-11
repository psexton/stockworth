import unittest
from datetime import date, timedelta

from stockworth.equity import Equity


class TestEquity(unittest.TestCase):

    def test_is_vested_by(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        tomorrow = today + timedelta(days = 1)
        instance = Equity(today.isoformat(), 100.0)

        self.assertEqual(instance.is_vested_by(tomorrow), True)
        self.assertEqual(instance.is_vested_by(today), True)
        self.assertEqual(instance.is_vested_by(yesterday), False)

    def test_from_rsu(self):
        vest_date = date(2020, 7, 8)
        shares = 5.0
        price = 12.5
        exp_value = shares * price
        instance = Equity.from_rsu(price, shares, vest_date.isoformat())

        self.assertEqual(instance.date, vest_date)
        self.assertEqual(instance.value, exp_value)

    def test_from_option(self):
        vest_date = date(2021, 2, 3)
        shares = 5.0
        current_price = 15.0
        strike_price = 14.0
        exp_value = (current_price - strike_price) * shares
        instance = Equity.from_option(current_price, shares, vest_date.isoformat(), strike_price)

        self.assertEqual(instance.date, vest_date)
        self.assertEqual(instance.value, exp_value)

    # Options can be worthless but they can't cost you money
    def test_from_underwater_option(self):
        shares = 5.0
        current_price = 10.0
        strike_price = 14.0
        exp_value = 0.0
        instance = Equity.from_option(current_price, shares, date.today().isoformat(), strike_price)

        self.assertEqual(instance.value, exp_value)


if __name__ == '__main__':
    unittest.main()
