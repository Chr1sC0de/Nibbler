import numpy as np
import pathlib as pt
import pandas as pd
import datetime as dt
import abc
from typing import Iterable
from .. math import greatestDivisor
from ..utils.timeframeconversion import (secondstotimeframe, timeframetoseconds)


class _NoneMarket:
    def __init__(self):
        self.name = None


class Feed(abc.ABC):

    def __init__(self):

        self._data     = np.zeros((1, 1))
        self._live     = np.zeros((1, 1))
        self.timedelta = None
        self.timeframe = None
        self._setdata()
        self._settimeframe()

        self._market   = _NoneMarket()
        self._master   = None
        self._counter  = None
        self._market   = None
        self._children = []

        self._maxiter = None
        self._maxind  = None

    def initialize(self):
        return iter(self)

    def step(self):
        return next(self)

    def setmaster(self, master: "Feed"):
        assert isinstance(master, Feed)
        self._master = master
        master.setchild(self)

    def delmaster(self):
        if self in self._master._children:
            self._master._children.remove(self)
        self._master = None

    def setchild(self, child: "Feed"):
        assert isinstance(child, self.__class__)
        if child not in self._children:
            self._children.append(child)

    def delchild(self, child: "Feed"):
        if child in self._children:
            child.delmaster()

    def delchildren(self):
        for child in self._children:
            self.delchild(child)

    def setmarket(self, market: "Market"):
        self._market = market

    @abc.abstractmethod
    def _setdata(self):
        NotImplemented

    def _settimeframe(self):
        self.timedelta = int(self._data[0, 2] - self._data[0, 1])
        divisor        = greatestDivisor(self.timedelta, secondstotimeframe.keys())
        multiplier     = self.timedelta/divisor
        self.timeframe = "%d%s"%(multiplier, secondstotimeframe[divisor])

    def __iter__(self):
        self._counter = 0
        self._live    = self._data[:, self._counter, None]
        self._maxind  = len(self._data[0]) - 1
        self._maxiter = len(self._data[0])
        [iter(child) for child in self._children]
        return self

    def __next__(self):
        if self._master is not None:

            if len(self._master.datetime):
                latestdatetime = self._master.datetime[-1]
            else:
                latestdatetime = self.startdatetime

            ndatetime      = len(self.datetime) - 1

            if ndatetime < 0:
                ndatetime = 0

            while self._data[0, ndatetime+1] <= latestdatetime:
                ndatetime += 1
                if ndatetime + 1 >= self._maxind:
                    break

            self._live = self._data[:, :ndatetime]
            [next(child) for child in self._children]
            return self

        self._counter += 1
        if self._counter > self._maxiter:
            self._counter = None
            return StopIteration

        self._live = self._data[:, :self._counter]
        [next(child) for child in self._children]
        return self

    def __getitem__(self, args: Iterable):
        return self._live[args]

    def __len__(self):
        return self._live.shape[-1]

    def __repr__(self):
        if self._counter is None:
            starttime  = dt.datetime.fromtimestamp(self._data[0][0]/1000)
            latesttime = dt.datetime.fromtimestamp(self._data[0][-1]/1000)
            return "<%s timeframe: %s period: %s to %s idle>"%(
                self.__class__.__name__, self.timeframe, starttime, latesttime
            )

        starttime   = dt.datetime.fromtimestamp(self._live[0][0]/1000)
        latesttime  = dt.datetime.fromtimestamp(self._live[0][-1]/1000)
        outpustring = "<%sFeed %s period:%s to %s "%(
            self.__class__.__name__, self._market.name, starttime, latesttime)
        outpustring += self._objectdata()
        outpustring += ">"
        return outpustring

    @abc.abstractmethod
    def _objectdata(self):
        return ""

    @property
    def shape(self):
        return self._live.shape

    @property
    def datetime(self):
        return self._live[0]

    @property
    def currentdatetime(self):
        return self.datetime[-1]

    @property
    def startdatetime(self):
        return self._data[0, 0]

    @abc.abstractmethod
    def plot(self, ax=None, *args, **kwargs):
        NotImplemented