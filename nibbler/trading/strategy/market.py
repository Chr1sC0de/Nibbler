
import numpy as np
from . import Strategy

class MarketLong(Strategy):

    def __call__(self, data):
        data.columns = data.columns.str.lower()
        if not self.in_trade:
            if self.buy_signal(data):
                self.buy(data)
        else:
            if self.TRADETARGET is not None:
                if data.high >= self.TRADETARGET:
                    self.sell(data)
            elif self.TRADESTOP is not None:
                if data.low <= self.TRADESTOP:
                    self.sell(data)
            elif self.sell_signal(data):
                self.sell(data)
