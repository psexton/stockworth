from datetime import date

class EquityGroup:
    def __init__(self, equity_list):
        self.equity_list = equity_list
        self.vesting_dates = set(e.date for e in equity_list)

    def total_value(self):
        return sum(e.value for e in self.equity_list)

    def vested_value(self):
        return self.value_at(date.today())

    def value_at(self, target_date):
        # partition equity_list by vesting_date
        # sum the ones with a vesting_date <= target_date
        return sum(e.value for e in self.equity_list if e.is_vested_by(target_date))
