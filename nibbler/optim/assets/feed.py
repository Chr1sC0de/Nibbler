import pandas as pd
import numpy as np
from pathlib import Path
import re


def check_inputs_(csv_file, nskip, wait):

    assert wait > 0, "wait time must be greater or equal to 1"
    assert nskip > 0, "nskip must be greater or equal to 1"

    assert isinstance(nskip, int), "nskip must be an integer"
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
        "pandas_data", "nskip",
        "data", "n", "max_len",
        "wait", "counter",
        "timeframe"
    ]

    def __init__(
        self,
        csv_file: Path,
        timeframe:str = None,
        nskip: int = 500,
        wait: int = 1
    ):

        csv_file = Path(csv_file)

        if timeframe is None:
            self.timeframe = get_timeframe_from_feed_(csv_file)

        check_inputs_(csv_file, nskip, wait)

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
        self.nskip = nskip//wait
        self.wait = wait

    def __len__(self):

        return self.max_len * self.wait

    def __iter__(self):

        self.wait = int(self.wait)
        self.counter = 0
        self.n = int(self.nskip) - 1
        return self
    
    def __next__(self):

        if self.counter%self.wait == 0:

            if self.n > self.max_len:
                raise StopIteration

            self.n += 1
            self.counter += 1

        self.counter += 1
        return self.data[:, 0:self.n]