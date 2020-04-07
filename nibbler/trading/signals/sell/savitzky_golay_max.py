try:
    from nibbler.trading.signals import SellSignal
    from nibbler.trading.indicators.trend import SavitzkyGolayHigh
    from nibbler.trading.math import max_finder
except:
    from .. import SellSignal
    from ...indicators.trend import SavitzkyGolayHigh
    from ...math import max_finder

import numpy as np

class SavitzkyGolayMax(SellSignal):

    def clean(self):
        super().cleans()
        del self.past_signalled_features

    @classmethod
    def random_initialization(cls, **kwargs):
        return cls(SavitzkyGolayMax.random_initialization(**kwargs))

    def __init__(self, *args, lag=20, **kwargs):
        if len(args) == 0:
            super().__init__(SavitzkyGolayHigh(**kwargs))
        else:
            super().__init__(*args)
        self.lag=lag
        self.past_signalled_features = []

    def generate_features(self, dataframe):
        original_length = len(dataframe)
        if len(dataframe > 1000):
            dataframe = dataframe.iloc[-1000:]
        difference = original_length - len(dataframe)
        features = self.indicators[0](dataframe)
        features = max_finder(features)
        features = np.argwhere(features).squeeze()
        try:
            return np.array(features)+difference
        except:
            return features

    def __call__(self, dataframe):
        N = len(dataframe)
        features = self.generate_features(dataframe)
        latest_time_features = features[-1]
        try:
            if (latest_time_features + self.lag) > N:
                if latest_time_features in self.past_signalled_features:
                    return False
                else:
                    self.signalled.append(latest_time_features)
                    self.past_signalled_features.append(latest_time_features)
                    return True
        except:
            return False