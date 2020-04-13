try:
    from nibbler.trading.signals import BuySignal
    from nibbler.trading.indicators.trend import SavitzkyGolayLow, SavitzkyGolayHigh
    from nibbler.trading.math import max_finder, min_finder
except:
    from .. import BuySignal
    from ...indicators.trend import SavitzkyGolayLow, SavitzkyGolayHigh

import talib
import numpy as np

class Candlestick(BuySignal):
    @classmethod
    def random_initialization(cls, **kwargs):
        return cls(
            SavitzkyGolayLow.random_initialization(**kwargs),
            SavitzkyGolayHigh.random_initialization(**kwargs)
        )

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            super().__init__(
                SavitzkyGolayLow(**kwargs),
                SavitzkyGolayHigh(**kwargs)
            )
        else:
            super().__init__(*args)

        self.past_signalled_features = []

    def generate_features(self, dataframe):
        original_length = len(dataframe)
        if len(dataframe) > 500:
            dataframe = dataframe.loc[-500:]
        else:
            pass

        difference = original_length - len(dataframe)

        filtered_low = self.indicators[0](dataframe)
        filtered_high = self.indicators[1](dataframe)

        maxes = np.argwhere(max_finder(filtered_high)).squeeze()
        lows = np.argwhere(min_finder(filtered_low)).squeeze()

        features = self.candlestickmethod(dataframe)

        # for debugging we can use this to show the feature data
        # disable this when training to maximize speed

        # for doji in dojis:
        #     closest_max = maxes[maxes<doji][-1]
        #     closest_min = lows[lows<doji][-1]
        #     try:
        #         if closest_min > closest_max:
        #             feature_dojos.append(doji)
        #     except:
        #         pass

        # return np.array(feature_dojos).squeeze()

        if lows[-1] > maxes[-1]:
            return [features[-1]+difference,]
        else:
            return [ ]

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLDOJI(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

    def __call__(self, dataframe):
        N = len(dataframe)
        features = self.generate_features(dataframe)
        try:
            latest_time_features = features[-1]
            if latest_time_features == N-1:
                return True
            else:
                return False
        except:
            return False