import locale

class Equity:
    def __init__(self, date, value):
        self.date = date
        self.value = value

    def __repr__(self):
        return f"({self.date} -> {locale.currency(self.value)})"

    @staticmethod
    def from_rsu(current_price, quantity, vest_date):
        value = current_price * quantity
        return Equity(vest_date, value)

    @staticmethod
    def from_option(current_price, quantity, vest_date, strike_price):
        purchase_price = quantity * strike_price
        sale_price = current_price * quantity
        value = sale_price - purchase_price
        return Equity(vest_date, value)
