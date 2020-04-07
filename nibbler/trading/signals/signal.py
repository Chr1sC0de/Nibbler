
from collections import OrderedDict
from ..indicators import Indicator
from ... import plot
import numpy as np

class Signal:

    def clean(self):
        del self.signalled

    @classmethod
    def random_initialization(cls):
        NotImplemented

    def __init__(self, *indicators):
        self.indicators_dict = OrderedDict()
        self.target = None
        self.stop = None
        self.signalled = []
        for indicator in indicators:
            assert issubclass(indicator.__class__, Indicator)
            if indicator.__class__.__name__ in self.indicators_dict.keys():
                counter = 0
                for name in self.indicators_dict.keys():
                    if indicator.__class__.__name__ in name:
                        counter +=1
                name = indicator.__class__.__name__ + f"_{counter}"
            else:
                name = indicator.__class__.__name__

            self.indicators_dict[name] = indicator

        self.indicators = [
            self.indicators_dict[key] for key in self.indicators_dict.keys()
        ]

    def generate_features(self, data_frame):
        NotImplemented

    def __call__(self, data_frame, calculate_stop=False):
        NotImplemented

    def save(self, path):
        np.save(path, self)

    def __repr__(self):
        output_string = ""
        for key, value in self.indicators_dict.items():
            output_string += key
            output_string += "\n"
            for parameter in self.indicators_dict[key].parameters.keys():
                output_string += f"    {parameter}: {self.indicators_dict[key].parameters[key]}"
                output_string += "\n"
        return output_string


class BuySignal(Signal):

    def plot_features(self, dataframe, fig=None, size=20, **kwargs):
        if fig is None:
            p = plot.candlesticks(dataframe)
        else:
            p = fig

        dataframe = plot.utils.lower_column_headers(dataframe)

        indices = self.generate_features(dataframe)

        low_values = dataframe.low.iloc[indices]

        date_time = dataframe.datetime.iloc[indices]

        p.triangle(
            date_time, low_values - 0.002 * low_values,
            size = size, color="green", alpha=0.5
        )

        return p

    def plot_signal(self, dataframe, fig=None, size=20, **kwargs):
        if fig is None:
            p = plot.candlesticks(dataframe)
        else:
            p = fig

        if self.signalled[-1] == len(dataframe):
            low_values = dataframe.low.iloc[-1]

            date_time = dataframe.datetime.iloc[-1]

            p.triangle(
                date_time, low_values - 0.002 * low_values,
                size = size, color="gold", alpha=0.5
            )
            return p
        else:
            return p

class SellSignal(Signal):


    def plot_signal(self, dataframe, fig=None, size=20, **kwargs):
        if fig is None:
            p = plot.candlesticks(dataframe)
        else:
            p = fig

        if self.signalled[-1] == len(dataframe):
            low_values = dataframe.low.iloc[-1]

            date_time = dataframe.datetime.iloc[-1]

            p.inverted_triangle(
                date_time, low_values + 0.002 * low_values,
                size = size, color="gold", alpha=0.5
            )

            return p
        else:
            return p

    def plot_features(self, dataframe, fig=None, size=20, **kwargs):
        if fig is None:
            p = plot.candlesticks(dataframe)
        else:
            p = fig
        dataframe = plot.utils.lower_column_headers(dataframe)

        indices = self.generate_features(dataframe)

        high_values = dataframe.high.iloc[indices]

        date_time = dataframe.datetime.iloc[indices]

        p.inverted_triangle(
            date_time, high_values + 0.002 * high_values,
            size = size, color="red", alpha=0.5
        )

        return p
