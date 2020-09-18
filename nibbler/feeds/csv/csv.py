from ..feed import Feed
import pathlib as pt
import pandas as pd
import numpy as np
import abc


class CSV(Feed):

    def __init__(self, csv_path: pt.Path):
        self.path               = pt.Path(csv_path)
        self._dataframe         = pd.read_csv(csv_path)
        self._dataframe.columns = self._dataframe.columns.str.lower()
        super(CSV, self).__init__()