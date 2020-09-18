from ..binance import TradingAgentSpecialEntries
import pandas as pd
import numpy as np
import time


class NibblerAllInAgent(TradingAgentSpecialEntries):

    def __init__(
            self, collector, bull_signal, bear_signal, *args, **kwargs
        ):
        self.collector = collector
        self.bull_signal = bull_signal
        self.bear_signal = bear_signal
        super().__init__(*args, **kwargs)
    
    def run(self):

        spaced_retries = 5

        while True:

            csv_file = "%s.csv"
            init = '2013-01-01T00:00:00Z'
            self.collector.run(csv_file, timestamp=init,  multiplier=1)
            data = pd.read_csv(csv_file)
            data.columns = data.colums.str.lower()

            if not self.in_trade:
                if self.bull_signal(data):
                    self.buy(data)
            else:

                if not self.stop_raised:
                    if data.close.iloc[-1] > (
                        self.TRADEOPEN + 0.5*(self.TRADEOPEN - self.TRADESTOP)
                    ):
                        self.TRADESTOP = self.TRADEOPEN + 0.25*(self.TRADEOPEN - self.TRADESTOP)
        
                if self.in_trade:
                    if self.TRADESTOP is not None:
                        if data.low.iloc[-1] <= self.TRADESTOP:
                            self.sell(data)
                            self.stop_raised = False
        
                if self.in_trade:
                    if data.close.iloc[-1] > (self.TRADEOPEN + 1.5*(self.TRADEOPEN - self.TRADESTOP)):
                        if self.bear_signal(data):
                            self.sell(data)
                            self.stop_raised = False

            if spaced_retries > 0:
                time.sleep(1)
                spaced_retries -= 1
            else:
                differnce = data['datetime'].iloc[-1] - data['datetime'].iloc[-2]
                next_time = data['datetime'].iloc[-1] + differnce

                current_time = time.time() * 1000
                wait_time = (next_time - current_time) * 1000

                time.sleep(wait_time)

            
    def buy(self, data):
        self.in_trade = True
        self.market_buy_order(quantity=self.get_quantity())
        self.TRADEOPEN = self.get_symbol_position().entryPrice
        if self.stop_calculator is not None:
            self.stop_calculator(self, data)



    def sell(self, data):
        position = self.get_symbol_position()
        self.market_sell_order(quantity=position)
        self.in_trade = False
            
    def get_quantity(self):
        balance = self.get_balance()
        ask = np.float(self.get_asks()['price'].iloc[0])
        quantity = balance/ask
        quantity = np.around(quantity, decimals=self.precision_quatity)
        return quantity