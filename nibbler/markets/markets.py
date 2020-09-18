import abc
from typing      import Iterable
from collections import defaultdict, OrderedDict
from ..utils     import timeframeconversion


class Market(abc.ABC):

    kind     = None
    makerfee = None
    takerfee = None

    def __init__(self, pair1: str, pair2: str, slippage=None):
        '''
        Slippage is a function which takes in the quantity to be bought and the .
        by defualt there is no slippage
        '''
        self.pair1             = pair1
        self.pair2             = pair2
        self.name              = "%s%s"%(self.pair1, self.pair2)
        self.exchange          = None
        self.timeframesmallest = 0
        self.masterkey         = None
        self.feeds             = {}
        self.feedsohlcv        = {}
        self.orders            = defaultdict(OrderedDict)
        self.stops             = defaultdict(OrderedDict)
        self._children         = []
        self._master           = None

        if slippage is None:
            self._slippage = lambda quantity, market: quantity

    def slippage(self, quantity):
        return self._slippage(quantity, self)

    def setmaster(self, mastermarket: "Market"):
        assert isinstance(mastermarket, Market)
        self.masterfeed.setmaster(mastermarket.masterfeed)
        mastermarket.setchild(self)

    def delmaster(self):
        self.masterfeed.delmaster()
        if self in self.masterfeed._children:
            self.masterfeed._children.remove(self)

    def setchild(self, child: "Market"):
        assert isinstance(child, Market)
        if child not in self._children:
            self._children.append(child)

    def delchild(self, child: "Master"):
        if child in self._children:
            child.delmaster()

    def delchildren(self):
        for child in self._children:
            self.delchild(child)

    def setexchange(self, exchange: "Exchange"):
        self.exchange = exchange

    def addfeeds(self, *feeds: "Feed"):
        for feed in feeds:
            feedkey = f"{feed.__class__.__name__}_{feed.timeframe}"
            if len(self.feeds) == 0:
                self.timeframesmallest = feed.timeframe
                self.masterkey         = feedkey
            elif feed.timedelta <= self.masterfeed.timedelta:
                self.timeframesmallest = feed.timeframe
                self.masterkey         = feedkey
            self.feeds[feedkey] = feed
            if feed.__class__.__name__ == "OHLCV":
                self.feedsohlcv[feed.timeframe] = feed

    def addorders(self, *orders):
        for order in orders:
            orderdictionary = self.orders[order.trader]
            orderid = len(orderdictionary)
            if orderid in orderdictionary.keys():
                while orderid in orderdictionary.keys():
                    orderid += 1
            orderdictionary[orderid] = order
            order.id = orderid

    def addstops(self, *stops):
        for stop in stops:
            stopdictionary = self.stops[stop.trader]
            stopid = len(stopdictionary)
            if stopid in stopdictionary.keys():
                while stopid in stopdictionary.keys():
                    stopid += 1
            stopdictionary[stopid] = stop
            stop.id = stopid

    def initialize(self):
        return iter(self)

    def step(self):
        return next(self)

    def __iter__(self):
        for key, feed in self.feeds.items():
            if key != self.masterkey:
                feed.setmaster(self.masterfeed)
        self.masterfeed.initialize()
        return self

    def __next__(self):
        self.masterfeed.step()
        [child.step() for child in self._children]
        # process each of the orders
        for orderdict in self.orders.values():
            orderdict_keys = list(orderdict.keys())
            for key in orderdict_keys:
                orderdict[key].process()
        # now process each of the stops
        for stopdict in self.stops.values():
            stopdict_keys = list(stopdict.keys())
            for key in stopdict_keys:
                stopdict[key].process()
        return self

    def __getitem__(self, key):
        if key in self.feeds.keys():
            return self.feeds[key]
        elif key in self.feedsohlcv.keys():
            return self.feedsohlcv[key]

    def __len__(self):
        return len(self.masterfeed)

    @property
    def masterfeed(self):
        return self.feeds[self.masterkey]
    @property
    def masterfeedohlcv(self):
        return self.feedsohlcv[self.timeframesmallest]

    @property
    def startdatetime(self):
        return self.masterfeed.startdatetime

    @property
    def allfeednames(self):
        return [name for name in self.feeds.keys()]
    @property
    def allohlcvfeednames(self):
        return [feed.timeframe for feed in self.feedsohlcv.values()]

    @property
    def currentdatetime(self):
        return self.masterfeedohlcv.currentdatetime
    @property
    def currentopen(self):
        return self.masterfeedohlcv.currentopen
    @property
    def currenthigh(self):
        return self.masterfeedohlcv.currenthigh
    @property
    def currentlow(self):
        return self.masterfeedohlcv.currentlow
    @property
    def currentclose(self):
        return self.masterfeedohlcv.currentclose
    @property
    def currentvolume(self):
        return self.masterfeedohlcv.currentvolume

    def __repr__(self):
        return f"<{self.name} {self.kind}Market feeds={self.allfeednames}"

    def plot(self, ax=None, **kwargs):
        '''
            if ax is None
        '''
        if any([ax is None, not isinstance(ax, Iterable)]):
            for feed in self.feedsohlcv.values():
                feed.plot(ax=ax, **kwargs)
            return ax
        for feed, axes in zip(self.feedsohlcv.values(), ax):
            output = feed.plot(ax=axes, **kwargs)
        return output

    def plot_masterohlcv(self, ax=None, **kwargs):
        return self.masterfeedohlcv.plot(ax=ax, **kwargs)

    def plot_orders(self, ax=None, **kwargs):
        for orderdict in self.orders.values():
            for order in orderdict.values():
                order.plot(ax=ax, **kwargs)

    def plot_stops(self, ax=None, **kwargs):
        for stopdict in self.stops.values():
            for stop in stopdict.values():
                stop.plot(ax=ax, **kwargs)
