import numpy as np
from bokeh.layouts import column, row
from ... import plot

class Strategy:
    def __init__(
        self,
        buy_signal,
        sell_signal,
        initial_account_balance = 1000,
        stop_calculator = None,
        target_calculator = None,
        slippage_frac = 0.0001,
        maker_fee_frac = 0.001,
        taker_fee_frac = 0.001,
        max_leverage = 100,
        use_leverage = False,
        leverage = 1,
        nskip = 500
    ):
        assert leverage < max_leverage
        self.nskip = nskip

        self.initial_account_balance = initial_account_balance
        self.account_balance = initial_account_balance

        self.buy_signal = buy_signal
        self.sell_signal = sell_signal
        self.stop_calculator = stop_calculator
        self.target_calculator = target_calculator

        self.slippage_frac = slippage_frac
        self.maker_fee_frac = maker_fee_frac
        self.taker_fee_frac = taker_fee_frac

        self.max_leverage = max_leverage
        self.use_leverage = use_leverage
        self.leverage = leverage

        self.TRADEOPEN = None
        self.TRADECLOSE = None
        self.TRADESTOP = None
        self.TRADETARGET = None
        # logging information

        self.trade_log = None

        self.balance_history = [self.initial_account_balance]
        self.won = 0
        self.lost = 0
        self.win_log = []
        self.lost_log = []
        self.avg_win_percent = 0
        self.avg_loss_percent = 0
        self.biggest_win_percent = 0
        self.biggest_loss_percent = 0
        self.buy_stamp = []
        self.sell_stamp = []
        self.percent_wins_total = 0

        self.liquidation_price = None
        self.fees = None

        self.position_amount = None
        self.asset_amount = None

        self.in_trade = False

        self.stop_raised = False 

    def walk_dataset(self, data):
        self.full_dataset = data
        N = len(data) - self.nskip
        data.columns = data.columns.str.lower()
        for k in np.arange(N):
            if self.is_liquidated(data):
                break
            else:
                self(data[0:(k+self.nskip)])
        if self.in_trade:
            self.sell(data)


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

    def buy(self, data):
        NotImplemented

    def sell(self, data):
        NotImplemented

    def build_trade_log(self, percent_wins, win_loss_value):
        self.percent_wins_total = percent_wins
        self.trade_log = \
            f'''
            initialBalance  : %f
            accountBalance  : %f
            no wins         : %d
            no losses       : %d
            percentWins     : %f
            avgWinPerTrade  : %f
            avgLossPerTrade : %f
            ''' % (
                   self.initial_account_balance, self.account_balance,
                   self.won, self.lost, percent_wins,
                   self.avg_win_percent, self.avg_loss_percent)

    def log_loss(self, pnl_percent):
        self.lost += 1
        self.lost_log.append(pnl_percent)
        self.avg_loss_percent = sum(self.lost_log)/len(self.lost_log)
        if pnl_percent < self.biggest_loss_percent:
            self.biggest_loss_percent = pnl_percent

    def log_win(self, pnl_percent):
        self.won += 1
        self.win_log.append(pnl_percent)
        self.avg_win_percent = sum(self.win_log)/len(self.win_log)
        if pnl_percent > self.biggest_win_percent:
            self.biggest_win_percent = pnl_percent

    def is_liquidated(self, data):
        if self.liquidation_price is None:
            return False
        # as there ca be minor floating point errors
        # we must add a small eps to the liquidation price
        elif data.low.iloc[-1] < (self.liquidation_price + 1e-5):
            self.in_trade = False
            self.account_balance = 0
            return True
        else:
            return False

    def long_with_slippage(self, data):
        return data.close.iloc[-1] \
            + data.close.iloc[-1] * self.slippage_frac

    def position_calculator(self, data):
        NotImplemented

    def plot_trades(self, fig = None, size = 20, width=1300, height=500):
        p = plot.utils.initialize_figure(
            fig, plot_width=width, plot_height=height)
        if fig is None:
            p = plot.candlesticks(self.full_dataset, fig=p)

        # plot buys
        date_time = self.full_dataset.datetime.iloc[self.buy_stamp]
        low_values = self.full_dataset.low.iloc[self.buy_stamp]
        p.triangle(
            date_time, low_values - 0.002 * low_values,
            size = size, color="green", alpha=0.5
        )
        # plot the sells
        date_time = self.full_dataset.datetime.iloc[self.sell_stamp]
        high_values = self.full_dataset.high.iloc[self.sell_stamp]
        p.inverted_triangle(
            date_time, high_values + 0.002 * high_values,
            size = size, color="red", alpha=0.5,
        )
        return p

    def plot_equity(self, fig=None, width=1300, height=500, **kwargs):
        p = plot.utils.initialize_figure(
            fig, plot_width=width, plot_height=height)
        date_time = self.full_dataset.datetime.iloc[self.sell_stamp]
        p.line(
            date_time, self.balance_history,
        )
        return p

    def plot_trade_and_equity(self, share_axis=True):
        p1 = self.plot_trades()
        p2 = self.plot_equity()
        if share_axis:
            p2.x_range = p1.x_range

        p1.title.text = "Trades"
        p2.title.text = "Equity"

        return column(
            p1, p2
        )

    def save(self, path):
        np.save(path, self)