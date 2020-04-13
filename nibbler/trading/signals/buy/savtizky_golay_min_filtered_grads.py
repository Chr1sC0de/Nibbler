try:
    from nibbler.trading.signals import BuySignal
    from nibbler.trading.indicators.trend import SavitzkyGolayLow
    from nibbler.trading.math import min_finder_filtered_grads, make_odd
except:
    from .. import BuySignal
    from ...indicators.trend import SavitzkyGolayLow
    from ...math import min_finder_filtered_grads, make_odd

import numpy as np

class SavitzkyGolayMinFilteredGrads(BuySignal):

    def clean(self):
        super().cleans()
        del self.past_signalled_features

    @classmethod
    def random_initialization(cls, **kwargs):
        return cls(SavitzkyGolayLow.random_initialization(**kwargs))

    def __init__(self, *args, lag=20, **kwargs):
        if len(args) == 0:
            self.finder_kwargs = {}
            self.finder_kwargs["window_length"] = kwargs.get("window_length", 12)
            self.finder_kwargs["poly_order"] = kwargs.get("poly_order", 3)
            super().__init__(SavitzkyGolayLow(**kwargs))
        else:
            super().__init__(*args)
        self.lag = lag
        self.past_signalled_features = []

    def generate_features(self, dataframe):
        original_length = len(dataframe)
        if len(dataframe > 1000):
            dataframe = dataframe.iloc[-1000:]
        difference = original_length - len(dataframe)
        features = self.indicators[0](dataframe)
        indicator_parameters = self.indicators[0].parameters

        d_filter = make_odd(indicator_parameters['window_length']//2)
        poly_order = np.min(
            [indicator_parameters['polyorder'],
            make_odd(indicator_parameters['window_length']//2)]
        )

        if poly_order == d_filter:
            d_filter = int(make_odd(d_filter*1.5))

        features = min_finder_filtered_grads(
            features,
            window_length=d_filter,
            poly_order=poly_order
        )
        features = np.argwhere(features).squeeze()
        try:
            return np.array(features)+difference
        except:
            return features

    def __call__(self, dataframe):
        N = len(dataframe)
        features = self.generate_features(dataframe)
        try:
            latest_time_features = features[-1]
            if (latest_time_features + self.lag) > N:
                if latest_time_features in self.past_signalled_features:
                    return False
                else:
                    self.signalled.append(len(dataframe))
                    self.past_signalled_features.append(latest_time_features)
                    return True
        except:
            return False