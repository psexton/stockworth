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
        return date.today()  # @TODO
