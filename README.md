# Nibbler

A library for crypto algorithmic trading

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

## Data Collection
We provided a convenience wrapper over ccxt to simplify data collection. Data can be collected via collector classes found in the trading collectors module
````
nibbler.trading.collectors.{exchange}{asset}
````
For example collecting data from binance can be performed,
````
from nibbler import trading as td
from pathlib import Path
directory = Path(__file__).parent
filename = 'binance1h.csv'
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
The Indicator class wraps over functions which take in OHLCV information from a pandas dataframe. For example we can easily convert functions from the technical analysis https://technical-analysis-library-in-python.readthedocs.io/en/latest/ library into Indicators
````
import ta
from nibbler.trading import Indicators
# the rsi momentum indicator takes the form
# ta.momentum.rsi(close, n=14, fillna=False)
sma_indicator = Indicator(ta.trend.sma, n=21)
````
The Indicator class stores parameters of the function and integrate with time series prediction modules.

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
where ````scale_defaults```` scales the default arguments to set the maximum randmly initialized values. It is however reocmmended that the ````random_initialization```` be overridden for custom initializations. Also to generate static Indicators we can overide the ````__init__```` method of a child. For example let us generate a custom static indicator for savitzky golay filtering.

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