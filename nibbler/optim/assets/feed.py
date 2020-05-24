import pandas as pd
import numpy as np
from pathlib import Path
import re


def check_inputs_(csv_file, wait):

    assert wait >= 0, "wait time must be greater or equal to 0"

    assert isinstance(wait, int), "wait must be an integer"

    assert csv_file.exists()


timeframe_suffixes_ = ["m", "h", "d", "w", "M"]


def get_timeframe_from_feed_(file_path: Path):

    name = file_path.name

    for suffix in timeframe_suffixes_:

        matches = re.findall("[0-9]+%s"%suffix, name)

        if len(matches) > 0:
            timeframe = matches[0]
            return timeframe
    
    return None


class Feed:

    __slots__ = [
        "pandas_data", 
        "data", "n", "max_len",
        "wait", "counter", "wait_",
        "timeframe"
    ]

    def __init__(
        self,
        csv_file: Path,
        timeframe:str = None,
        wait: int = 0
    ):

        csv_file = Path(csv_file)

        if timeframe is None:
            self.timeframe = get_timeframe_from_feed_(csv_file)

        check_inputs_(csv_file, wait)

        self.pandas_data = pd.read_csv(csv_file)

        self.pandas_data.columns = self.pandas_data.columns.str.lower()

        self.set_data_()

        self.wait = wait

    def clip_dataframe(self, start, end):

        if self.wait == 0:
            self.pandas_data = self.pandas_data.iloc[start: end//1]
        else:
            self.pandas_data = self.pandas_data.iloc[start: end//self.wait]
        self.set_data_()

    def __len__(self):

        self.set_data_()

        if self.wait == 0:
            return self.data.shape[-1]
        else:
            return self.data.shape[-1] * self.wait
    
    def set_data_(self):

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

    def __iter__(self):

        self.set_data_()

        self.max_len = len(self)
        self.wait_ = int(self.wait + 1)
        self.counter = 0
        self.n = 0

        return self
    
    def __next__(self):

        if self.counter%self.wait_ == 0:

            if self.n > self.max_len:
                raise StopIteration

            self.n += 1
            self.counter += 1

        self.counter += 1

        return self.data[:, 0:self.n]