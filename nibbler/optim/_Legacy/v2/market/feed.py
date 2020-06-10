import numpy as np
import abc
from ...math import greatestDivisor

timeframeDict = {
    1000*60:"m",
    1000*60*60:"h",
    1000*60*60*24:"d",
    1000*60*60*24*7:"w"
}


def _is_int_and_greater_than_zero(value):
    if not isinstance(value, int):
        raise ValueError(f"value {value} is not an int")
    if not value >= 0:
        raise ValueError(f"value {value} is not greater than or equal to 0")


class Feed(abc.ABC):


    timeframeDict = {
        1000*60:"m",
        1000*60*60:"h",
        1000*60*60*24:"d",
        1000*60*60*24*7:"w"
    }


    timeframeSuffixes = ["m", "h", "d", "w", "M"]

    def __init__(self, delay:int=0, wait: int=0):
        self.set_delay(delay)
        self.set_wait(wait)

        # dummy variable to make the data array iterable
        self._data = np.ones((6, 1))
        self._set_data()
        self._set_timeframe()

    def _set_timeframe(self):
        self.timeDelta = int(self._data[0, 2] - self._data[0, 1])
        divisor = greatestDivisor(self.timeDelta, timeframeDict.keys())
        multiplier = self.timeDelta/divisor
        self.timeframe = "%d%s"%(multiplier, timeframeDict[divisor])

    def start_time(self):
        return self._data[0, 0]

    def end_time(self):
        return self._data[0, -1]

    def set_delay(self, delay):
        _is_int_and_greater_than_zero(delay)
        self._delay = delay

    def set_wait(self, wait):
        _is_int_and_greater_than_zero(wait)
        self._wait = wait + 1

    def clip_feed(self, start, end):
        self._data = self._data[:, start:end]

    @abc.abstractmethod
    def _set_data(self):
        '''
            the data is an numpy array (data, feed)
            we assume data=[datetime, open, high, low, close volume]
        '''
        NotImplemented

    def __len__(self):
        return self._delay + self._data.shape[-1] * self._wait

    def __iter__(self):

        self._max_snip = len(self)

        self._snip = 0
        self._counter = 0

        self._delay_ = self._delay

        return self

    def __next__(self):

        if self._delay_ <= 0:

            if self._counter%self._wait==0:

                self._snip += 1
                self._counter += 1

                if self._snip > self._max_snip:
                    raise StopIteration

                return self._data[:, 0:self._snip]

            self._counter+=1
        else:
            self._delay_ -= 1
            return None

