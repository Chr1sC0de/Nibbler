import numpy as np
from nibbler import plt
from .feed import Feed


_allnames = ["open", "high", "low", "close"]


class OHLCV(Feed):

    '''
    Abstract base class for a feed which contains open high low close and
    volume data
    '''
    # assign the tempdata in the constructor
    _tempdata = None

    def _setdata(self):
        self._data = self._tempdata

    def _objectdata(self):
        outputString = "OHLCV: %0.3f/%0.3f/%0.3f/%0.3f/%0.3f"
        return outputString%(
            self.currentopen, self.currenthigh,
            self.currentlow, self.currentclose,
            self.currentvolume
        )

    @property
    def open(self):
        return self._live[1]
    @property
    def high(self):
        return self._live[2]
    @property
    def low(self):
        return self._live[3]
    @property
    def close(self):
        return self._live[4]
    @property
    def volume(self):
        return self._live[5]

    @property
    def currentopen(self):
        return self.open[-1]
    @property
    def currenthigh(self):
        return self.high[-1]
    @property
    def currentlow(self):
        return self.low[-1]
    @property
    def currentclose(self):
        return self.close[-1]
    @property
    def currentvolume(self):
        return self.volume[-1]

    def plot_stream(
        self, datastream,
        ax=None, name=None,
        color="r", alpha=1, linewidth=2,
        **kwargs
    ):
        if ax is None:
            ax = plt.gca()
        datetime = plt.utils.convertTimestampToDatetime(
            self.datetime)
        ax.plot_date(
            datetime, datastream,
            "-",
            color     = color,
            linewidth = linewidth,
            **kwargs
        )
        return ax

    def plot(
        self, ax=None, vax=None, feednames=None, showvolume=True,
        tailwidth = 1.0, bodywidth=1.5, ylabel="Price",
        c_open="g", c_close="r", c_highlow="k",
        alpha_tail=0.6,
        **kwargs
    ):
        if ax is None:
            ax = plt.gca()

        if feednames is None:
            feednames = _allnames
        else:
            for name in feednames:
                assert name in _allnames, f"feeds names must be in {_allnames}"
        datetime = plt.utils.convertTimestampToDatetime(self.datetime)
        ax.plot_date(datetime, self.open, c_open, **kwargs)
        ax.plot_date(datetime, self.close, c_close, **kwargs)
        kwargs.pop("alpha", None)
        ax.plot_date(
            datetime, self.high, c_highlow, alpha=alpha_tail, **kwargs)
        ax.plot_date(
            datetime, self.low, c_highlow, alpha=alpha_tail, **kwargs)
        if showvolume:
            if vax is not None:
                plt.volumeOnScreen(self, ax=vax)
                return ax
            ax = plt.volumeOnScreen(self, ax=ax)
        return ax