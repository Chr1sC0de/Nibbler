import numpy as np
import abc
import pathlib as pt
import pandas as pd
from ...math import greatestDivisor
from .. import timeframeToSeconds, secondsToTimeframe


def _is_int_and_greater_than_zero(value):
    if not isinstance(value, int):
        raise ValueError(f"value {value} is not an int")
    if not value >= 0:
        raise ValueError(f"value {value} is not greater than or equal to 0")

class Feed(abc.ABC):

    def __init__(self):
        self.data = np.ones((6,1))
        self._setData()
        self._setTimeframe()

    def _setTimeframe(self):
        self.timeDelta = int(self.data[0, 2] - self.data[0, 1])
        divisor = greatestDivisor(self.timeDelta, secondsToTimeframe.keys())
        multiplier = self.timeDelta/divisor
        self.timeframe = "%d%s"%(multiplier, secondsToTimeframe[divisor])

    @abc.abstractmethod
    def _setData(self):
        '''
            the data is an numpy array (data, feed)
            we assume data=[datetime, open, high, low, close volume]
        '''
        NotImplemented

    def __len__(self):
        return self.data.shape[-1]


class CSVFeed(Feed):

    def __init__(self, csv_path: pt.Path):
        self.csv_path = pt.Path(csv_path)
        self._dataframe = pd.read_csv(csv_path)
        self._dataframe.columns = self._dataframe.columns.str.lower()
        super().__init__()
    
    def _setData(self):
        self.data = np.stack(
           [
               self._dataframe["datetime"],
               self._dataframe["open"],
               self._dataframe["high"],
               self._dataframe["low"],
               self._dataframe["close"],
               self._dataframe["volume"]
           ], axis=0
        )
        del self._dataframe
    