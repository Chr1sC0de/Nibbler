from .trader import Trader
from nibbler import math
from nibbler import plt
import talib


class MinMax(Trader):

    def __init__(
        self,
        *args,
        market       = "BTCUSDT",
        window_long  = 144,
        window_short = 21,
        savgol_window = 13,
        polyorder    = 3,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.in_position = False
        self.window_long = window_long
        self.window_short = window_short
        self.svgol = math.filters.PolyfitSavgolFilter(
            window_size=savgol_window)

    def strategy(self):
        [wallet.log_balance() for wallet in self.spotwallets.values()]
        [wallet.log_balance() for wallet in self.marginwallets.values()]
        btc_market = self.exchange.spotmarkets["BTCUSDT"]
        if len(btc_market) > 10000:
            # filtered_data_long  = self.filter_long(btc_market["1m"].close)
            # filtered_data_short = self.filter_short(btc_market["1m"].close)
            filtered_data_long  = talib.TEMA(
                btc_market["1m"].close, self.window_long)
            filtered_data_long = self.svgol(filtered_data_long)

            # filtered_data_short = talib.TEMA(
            #     btc_market["1m"].close, self.window_short)
            # filtered_data_short = self.svgol(filtered_data_short)
            # filtered_data = talib.EMA(btc_market["1m"].close)
            btc_market["1m"].plot_stream(filtered_data_long, color="green")
            # btc_market["1m"].plot_stream(filtered_data_short, color="blue")
            btc_market["1m"].plot()
            plt.show()
            test       = 5
            pass


