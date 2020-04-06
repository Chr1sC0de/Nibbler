from ...math import (
    min_open, min_high, min_low, min_close
)
from .. import Indicator
from ....plot.utils import lower_column_headers, initialize_figure
import numpy as np


class MinFinderBase(Indicator):

    @classmethod
    def random_initialization(
            cls, min_window=1, max_window=20,
            min_poly=1, max_poly=5):
        window_length = np.random.randint(min_window, max_window)
        poly = np.random.randint(
            min_poly, np.min([max_poly, window_length])
        )
        return cls(window_length=window_length, polyorder=poly,
        deriv=0, delta=1.0, mode='interp', cval=0)

    def plot(self, dataframe, fig=None, size=20, **kwargs):
        p = initialize_figure(fig)
        dataframe = lower_column_headers(dataframe)

        indices = np.argwhere(self(dataframe)).squeeze()

        low_values = dataframe.low.iloc[indices]

        date_time = dataframe.datetime.iloc[indices]

        p.triangle(
            date_time, low_values - 0.002 * low_values,
            size = size, color="green", alpha=0.5
        )

        return p

class MinFinderOpen(MinFinderBase):
    def __init__(self, **kwargs):
        super().__init__(min_open, **kwargs)

class MinFinderHigh(MinFinderBase):
    def __init__(self, **kwargs):
        super().__init__(min_high, **kwargs)

class MinFinderLow(MinFinderBase):
    def __init__(self, **kwargs):
        super().__init__(min_low, **kwargs)

class MinFinderClose(MinFinderBase):
    def __init__(self, **kwargs):
        super().__init__(min_close, **kwargs)