from .feed import Feed
import pandas as pd
import pathlib as pt
import numpy as np


class CSVFeed(Feed):

    def __init__(self, csv_path: pt.Path, delay:int=0, wait: int=0):
        self.csv_path = pt.Path(csv_path)
        self._dataframe = pd.read_csv(csv_path)
        self._dataframe.columns = self._dataframe.columns.str.lower()
        super().__init__(delay=delay, wait=wait)
    
    def _set_data(self):
        self._data = np.stack(
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

