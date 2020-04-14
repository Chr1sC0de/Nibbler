import numpy as np
from . import Strategy

class MarketLong(Strategy):

    def __call__(self, data):

        data.columns = data.columns.str.lower()
        if not self.in_trade:
            if self.buy_signal(data):
                self.buy(data)
        else:

            if not self.stop_raised:
                if data.close.iloc[-1] > (self.TRADEOPEN + 0.5*(self.TRADEOPEN - self.TRADESTOP)):
                    self.TRADESTOP = self.TRADEOPEN + 0.25*(self.TRADEOPEN - self.TRADESTOP)
            
            if self.TRADETARGET is not None:
                if data.high.iloc[-1] >= self.TRADETARGET:
                    self.sell(data, self.TRADETARGET)
                    self.stop_raised = False
    
            if self.in_trade:
                if self.TRADESTOP is not None:
                    if data.low.iloc[-1] <= self.TRADESTOP:
                        self.sell(data, stop=None)
                        self.stop_raised = False
    
            if self.in_trade:
                if data.close.iloc[-1] > (self.TRADEOPEN + 1.5*(self.TRADEOPEN - self.TRADESTOP)):
                    if self.sell_signal(data):
                        self.sell(data)
                        self.stop_raised = False

    def buy(self, data):
        self.in_trade = True
        self.buy_stamp.append(len(data) - 1)

        self.TRADEOPEN = self.long_with_slippage(data)
        if self.stop_calculator is not None:
            self.stop_calculator(self, data[-self.nskip:])

        position = self.position_calculator(data)

        self.account_balance -= (
            position + self.fees
        )

    def sell(self, data, target=None, stop=None):
        self.sell_stamp.append(len(data)-1)
        self.in_trade = False
    
        if stop is not None:
            self.TRADECLOSE = self.TRADESTOP
        elif target is None:
            self.TRADECLOSE = data.close.iloc[-1]
        else:
            self.TRADECLOSE = target

        win_fraction = self.TRADECLOSE/self.TRADEOPEN

        trade = self.position_amount * win_fraction

        fee = trade * self.taker_fee_frac

        self.account_balance += (trade-fee)

        self.balance_history.append(self.account_balance)

        pnl_percent = (win_fraction - 1) * 100

        win_loss_value = trade - self.position_amount

        if pnl_percent < 0:
            self.log_loss(pnl_percent)
        if pnl_percent > 0:
            self.log_win(pnl_percent)

        if self.won + self.lost == 0:
            percent_wins = 0
        else:
            percent_wins = self.won/(self.won + self.lost)

        self.build_trade_log(percent_wins, win_loss_value)

    def position_calculator(self, data):
        # calculate the positions and fees
        # if applicable set the target and stop here as well

        # total_spent = position_size + fees
        # fees = position_size * taker_fee
        # total_spent = position_size * (1+taker_fee)
        if not self.use_leverage:
            self.position_amount = self.account_balance/(1+self.taker_fee_frac)
            self.fees = self.position_amount * self.taker_fee_frac
            self.asset_amount = self.position_amount/self.TRADEOPEN


        # for an accurate simulation this must be set when leverage is used
        else:
            self.position_amount = (self.account_balance*self.leverage)/(1+self.taker_fee_frac)
            self.fees = self.position_amount * self.taker_fee_frac
            self.asset_amount = self.position_amount/self.TRADEOPEN

            # the liquidation price is going to be when your account balance goes to 0
            # whilst holding leverage, this is not recommended when no stop is calculated

            # price_movement * asset amount = balance
            # price_movement = balace/asset_amount
            # liquidation_price = TRADEOPEN - price_movement
            self.liquidation_price =  self.TRADEOPEN - self.account_balance/self.asset_amount

        if self.stop_calculator is not None:
            # the stop calculator takes in the current stop
            self.TRADESTOP = self.stop_calculator(self, data)
        if self.target_calculator is not None:
            self.TRADETARGET = self.target_calculator(self, data)
        # signals will have a target attribute that is calcated
        # if a target is not calculated by a signal the signal will return None
        self.TRADETARGET = self.buy_signal.target

        return self.position_amount
