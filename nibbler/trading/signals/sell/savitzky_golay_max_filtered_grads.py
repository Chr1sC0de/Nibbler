try:
    from nibbler.trading.signals import SellSignal
    from nibbler.trading.indicators.trend import SavitzkyGolayHigh
    from nibbler.trading.math import max_finder_filtered_grads
except:
    from .. import SellSignal
    from ...indicators.trend import SavitzkyGolayHigh
    from ...math import max_finder_filtered_grads

import numpy as np

class SavitzkyGolayMaxFilteredGrads(SellSignal):

    def clean(self):
        super().cleans()
        del self.past_signalled_features

    @classmethod
    def random_initialization(cls, **kwargs):
        return cls(SavitzkyGolayHigh.random_initialization(**kwargs))

    def __init__(self, *args, lag=20, **kwargs):
        if len(args) == 0:
            self.finder_kwargs = {}
            self.finder_kwargs["window_length"] = kwargs.get("window_length", 12)
            self.finder_kwargs["poly_order"] = kwargs.get("poly_order", 3)
            super().__init__(SavitzkyGolayHigh(**kwargs))
        else:
            super().__init__(*args)
        self.lag=lag
        self.past_signalled_features = []

    def generate_features(self, dataframe):
        features = self.indicators[0](dataframe)
        indicator_parameters = self.indicators[0].parameters
        features = max_finder_filtered_grads(
            features,
            window_length=indicator_parameters['window_length'],
            poly_order=indicator_parameters['poly_order']
        )
        features = np.argwhere(features).squeeze()
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
                    self.signalled.append(latest_time_features)
                    self.past_signalled_features.append(latest_time_features)
                    return True
        except:
            return False