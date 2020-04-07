from .. import Indicator
from ...math import (
    savitzky_golay_close, savitzky_golay_high,
    savitzky_golay_low, savitzky_golay_open, make_odd
)
import numpy as np


class SavitzkyGolayBase(Indicator):
    @classmethod
    def random_initialization(cls,
            min_window=3, max_window=20,
            min_poly=3, max_poly=5):
        window_length = make_odd(np.random.randint(min_window, max_window))
        poly = np.random.randint(
            min_poly, np.min([max_poly, window_length])
        )
        return cls( window_length=window_length, polyorder=poly,
            deriv=0, delta=1.0, mode='interp', cval=0)

class SavitzkyGolayOpen(SavitzkyGolayBase):

    def __init__(self, **kwargs):
        super().__init__(savitzky_golay_open, **kwargs)


class SavitzkyGolayHigh(SavitzkyGolayBase):

    def __init__(self, **kwargs):
        super().__init__(savitzky_golay_high, **kwargs)


class SavitzkyGolayLow(SavitzkyGolayBase):

    def __init__(self, **kwargs):
        super().__init__(savitzky_golay_low, **kwargs)


class SavitzkyGolayClose(SavitzkyGolayBase):

    def __init__(self, **kwargs):
        super().__init__(savitzky_golay_close, **kwargs)