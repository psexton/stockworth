from datetime import date


class Threshold:
    def __init__(self, amount, equity_group):
        self.amount = amount
        self.equity_group = equity_group
        self.date = self._compute_date()

    def __repr__(self):
        return f"({self.amount} -> {self.date})"

    def _compute_date(self):
        # Need to compute when unvested equity will be less than the threshold amount
        # Subtract the threshold from the total equity value
        total_equity_value = self.equity_group.total_value()
        vested_at_threshold = total_equity_value - self.amount
        # Now iterate over equity vest dates, in ascending order,
        # until that value is >= the subtraction result
        vesting_dates = sorted(self.equity_group.vesting_dates)
        for vesting_date in vesting_dates:
            if self.equity_group.value_at(vesting_date) >= vested_at_threshold:
                return vesting_date
