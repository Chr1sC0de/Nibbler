import pandas as pd
import numpy as np
from pathlib import Path


class Feed:

    __slots__ = [
        "pandas_data", "nskip",
        "data", "n", "max_len",
        "wait", "counter"
    ]

    def __init__(self, csv_file, nskip=500, wait=1):

        csv_file = Path(csv_file)

        self.pandas_data = pd.read_csv(csv_file)
        self.pandas_data.columns = self.pandas_data.columns.str.lower()

        self.max_len = len(self.pandas_data)

        self.data = np.stack(
           [
               self.pandas_data["datetime"],
               self.pandas_data["open"],
               self.pandas_data["high"],
               self.pandas_data["low"],
               self.pandas_data["close"],
               self.pandas_data["volume"]
           ], axis=0
        )
        self.nskip = nskip
        self.wait = wait

    def __len__(self):

        return self.max_len * self.wait

    def __iter__(self):

        self.counter = 0
        self.n = self.nskip - 1
        return self
    
    def __next__(self):

        if self.counter%self.wait:

            if self.n > self.max_len:
                raise StopIteration

            self.n += 1
            self.counter += 1

            return self.data[:, 0:self.n]

        self.counter += 1