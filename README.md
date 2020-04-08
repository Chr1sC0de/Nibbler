# Nibbler

A degenerates library for algorithmic crypto trading.

The old way:
    Make a strat
    go live
    get bogged.
    get rekt.
    return zero

The new modern way:
    while True:
        Make a strat
        optimize
        go live
        moon
        buy lambo
        get chainlink
        lose it all

Welcome to crypto.

## Installation

To install requirements
````
python -m pip install -r requirements.txt
````
To install in symbolic mode,
````
python -m pip install -e .
````
To install in release mode,
````
python -m pip install .
````
To install TA-Lib, in the top of the directory,
````
python -m pip install TA_Lib-0.4.17-cp37-cp37m-win_amd64.whl
````

if you have a different version of python or os, download the correct version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

## Data Collection
We provide a convenience wrapper over ccxt to simplify data collection. Data can be collected via collector classes found in the trading collectors module
````
nibbler.trading.collectors.{exchange}{asset}
````
For example collecting data from binance can be performed,
````
from nibbler import trading as td
from pathlib import Path
directory = Path(__file__).parent
filename = {relative_filename}
filepath = directory/filename
collector = td.collectors.BinanceBTC('1h')
collector.run(filepath, multiplier=4)
````
Collectors run continuously until closed.

New collectors can be generated through inheritence of the Collector base class,
````
form nibbler.trading.collectors import Collector
class BinanceETH(Collector):
    _exchange = 'binance'
    symbol = 'ETH/USDT'
    limit = 1000

````
## Plotting Candlestick Data
Plotting of candlestick data is performed via bokeh.
````
from nibbler import plot
import pandas as pd

df = pd.read_csv({csv_file_path})
p = plot.candlesticks(df)
plot.show(p)
````
To plot directly from a csv file
````
p = plot.csv.candlesticks({csv_file_path})
plot.show(p)
````

## Indicators
The Indicator class wraps over functions which take in OHLCV information from a pandas dataframe. For example we can easily convert functions from the technical analysis https://technical-analysis-library-in-python.readthedocs.io/en/latest/ or https://github.com/mrjbq7/ta-lib library into Indicators
````
import ta
from nibbler.trading import Indicators
# the rsi momentum indicator takes the form
# ta.momentum.rsi(close, n=14, fillna=False)
sma_indicator = Indicator(ta.trend.sma, n=21)
````
The Indicator class stores parameters of the function and integrate with time series forecast modules.

The Indicator class also contains convenience methods for visualization and random initialization.

````
import pandas as pd
from nibbler import plot
df = pd.read_csv({path_to_csv_file})
indicator_results = sma_indicator(df)
# we can plot the resulting indicator onto a figure of candlesticks with the
# the follwing methods
p = plot.candlesticks(df)
sma_indicator.plot(df, fig = p)
plot.show(p)
````
An indicator can be randomly initialized,
````
Indicator.random_initialization({function}, scale_default=3)
````
where ````scale_defaults```` scales the default arguments to set the maximum randmly initialized values. It is however reocmmended that the ````random_initialization```` be overridden for custom Indicators.

To generate static Indicators we can overide the ````__init__```` method of a child. For example let us generate a custom static indicator for savitzky golay filtering.

````
import savitzky_golay_open

class SavitzkyGolayBase(Indicator):
    @classmethod
    def random_initialization(cls, min_window, max_window, min_poly, max_poly):
        window_length = np.random.randint(min_window, max_window)
        poly = np.random.randint(
            min_poly, np.min([max_poly, window_length])
        )
        return cls( window_length=window_length, polyorder=poly,
        deriv=0, delta=1.0, mode='interp', cval=0)

class SavitzkyGolayOpen(SavitzkyGolayBase):

    def __init__(self, **kwargs):
        super().__init__(savitzky_golay_open, **kwargs)
````
## Signals
Signals take in a data frame then output either a true or false buy or sell signal. Signals are constructed from a set of features extracted from indicators. These features are the index location of the candlesticks of interest. The final signal and its features can be plotted with the ````plot_features```` and ````plot_signals```` methods of the Signal object. Buy features are denoted as green triangles, whilst  sell signals are in red inverted triangles. The buy signal itself is a yellow triangle whilst the sell signals are inverted yellow triangles

````
from nibbler import plot
from nibbler.trading.signals.buy import SavitzkyGolayMin
import pathlib as pt
import pandas as pd

cwd = pt.Path(__file__).parent

resources_folder = cwd/"../../resources"

corn_file = resources_folder/"BitcoinBinance1hr.csv"

signal = SavitzkyGolayMin()

df = pd.read_csv(corn_file)[-100:]

signallled = signal(df)

p = signal.plot_features(df)
p = signal.plot_signal(df, fig=p)

signal.clean()
````
The clean method is used when optimizing a signal. Signals can retain memory of prior signals to allow for easier plotting and to ensure that a signal, when lagging, is not repeated when using the same dataset.

Custom signals are inherited from either the BuySignal or SellSignal classes. As an examples the following shows a min finder signal,

````
from nibbler.trading.signals import BuySignal
from nibbler.trading.indicators.trend import SavitzkyGolayLow
from nibbler.trading.math import min_finder

import numpy as np

class SavitzkyGolayMin(BuySignal):

    # this method handles any removals necessary when changing datasets
    def clean(self):
        super().cleans()
        del self.past_signalled_features

    # this class method handles the random initialization
    @classmethod
    def random_initialization(cls, **kwargs):
        return cls(SavitzkyGolayLow.random_initialization(**kwargs))

    # The init method requires two methods for when
    # the Signal is initialized deterministically or randomly
    def __init__(self, *args, lag=20, **kwargs):
        if len(args) == 0:
            super().__init__(SavitzkyGolayLow(**kwargs))
        else:
            super().__init__(args)
        self.lag = lag
        self.past_signalled_features = []

    # the generate features method is used to create the
    # features necessary for the signal to operate
    def generate_features(self, dataframe):
        features = self.indicators[0](dataframe)
        features = min_finder(features)
        features = np.argwhere(features).squeeze()
        # features are of the form [1, 10, 2567, 8999,... etc]
        return features

    # the call method parses the output features and
    # returns either a true or false statement
    def __call__(self, dataframe):
        N = len(dataframe)
        features = self.generate_features(dataframe)
        latest_time_features = features[-1]
        if (latest_time_features + self.lag) > N:

            if latest_time_features \
                    in self.past_signalled_features:
                return False
            else:
                self.signalled.append(len(dataframe))
                self.past_signalled_features.append(latest_time_features)
                return True
````

In the above signal, as it is lagging, the past min features must be stored and checked to avoid repeating a signal. These types of checks must be taken into consideration when designing a strategy.

## Strategies and Optimiztion
A trading strategy must take into consideration, to name a few, the following:
1. buy signal
2. stop
3. sell signal
4. entry method
5. target
6. exit method

### Strategies
Strategies are a combination of signals and risk management methods. The strategy class is constructed with the following structure

````
Class Strategy:
    def __init__(
        self,
        buy_signal,
        sell_signal,
        initial_account_balance = 1000,
        stop_calculator = None,
        slippage_frac = 0.0001,
        maker_fee_frac = 0.001,
        taker_fee_frac = 0.001,
        max_leverage = 100,
        use_leverage = False,
        leverage = 1
    ):
    def walk_dataset(self, data, nskip=100):
    def __call__(self, data):
    def buy(self, data):
        # Implemented By User
    def sell(self, data):
        # Implemented By User
    def position_calculator(self, data):
        # Implemented By User
    def build_trade_log(self, percent_wins, win_loss_value):
    def log_loss(self, pnl_percent):
    def log_win(self, pnl_percent):
    def is_liquidated(self, data):
    def long_with_slippage(self, data):
    def plot_trades(self, fig = None, size = 20, width=1300, height=500):
    def plot_equity(self, fig=None, width=1300, height=500, **kwargs):
    def plot_trade_and_equity(self, share_axis=True):
    def save(self, path):
````

A market long strategy can be implemented as follows,

````
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

    def buy(self, data):
        self.in_trade = True
        self.buy_stamp.append(len(data) - 1)

        self.TRADEOPEN = self.long_with_slippage(data)
        if self.stop_calculator is not None:
            self.stop_calculator(data)

        position = self.position_calculator(data)

        self.account_balance -= (
            position + self.fees
        )

    def sell(self, data):
        self.sell_stamp.append(len(data)-1)
        self.in_trade = False

        self.TRADECLOSE = data.close.iloc[-1]

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

````


### Brute Force Walk-Forward Optimization

Once we get here it is time to pit our little nibbler strategies into mono v mono mortal combat to see which strategy will live.
Initialize a population of strategies with ````Initialization```` methods,

````
    import nibbler as nd
    from nibbler.optim import BruteForceSingleDataset
    from nibbler.trading.signals.buy import SavitzkyGolayMinFilteredGrads
    from nibbler.trading.signals.sell import SavitzkyGolayMaxFilteredGrads
    from nibbler.trading.strategy import MarketLong
    from nibbler.initialization import MarketStrategyInitialization
    from nibbler import plot
    import pandas as pd
    import pathlib as pt

    # setttings for the signals and the strategy
    buy_signal_kwargs = dict(
        min_window=3, max_window=20,
        min_poly=3, max_poly=5
    )

    sell_signal_kwargs = dict(
        min_window=3, max_window=20,
        min_poly=3, max_poly=5
    )

    strategy_kwargs = dict(
        initial_account_balance = 1000,
        stop_calculator = None,
        slippage_frac = 0.0001,
        maker_fee_frac = 0.001,
        taker_fee_frac = 0.001,
        max_leverage = 100,
        use_leverage = False,
        leverage = 1
    )

    strategy_population = MarketStrategyInitialization(
        SavitzkyGolayMinFilteredGrads,
        SavitzkyGolayMaxFilteredGrads,
        MarketLong,
        buy_signal_kwargs,
        sell_signal_kwargs,
        strategy_kwargs,
        n_population=16
    )

    # this guard is necessary for enabling multiprocesssing
    if __name__ == "__main__":

        cwd = pt.Path(__file__).parent
        resource_folder = cwd/"../../resources"

        data_file = resource_folder/"BitcoinBinance1hr.csv"
        dataframe = pd.read_csv(data_file)

        optimizer = BruteForceSingleDataset(strategy_population)

        optimizer.calculate_fitness(dataframe.iloc[0:1000], n_processors=8)

        p = optimizer.population[-1].plot_trade_and_equity()

        plot.show(p)

        # save the best nibbler strategy, which contains the best nibtard, time to put em in the burner and go live
        # get ready to lose everything

        nd.save(
            pt.Path(__file__).parent/"best_lad",
            optimizer.population[-1]
        )
````

### Out of Sample Brute Force Optimization
    to do

### Brute Force Monte-Carlo Optimization
    to do

## Going Live
    Binance API agents currently created