from .. import timeframeToSeconds, secondsToTimeframe
import numpy as np
from collections import defaultdict, OrderedDict


class Market:

    def __init__(self, pair1, pair2, maxLeverage: float = 125, slippage=0):
        self.slippage = slippage
        self.pair1 = pair1
        self.pair2 = pair2
        self.name = "%s-%s"%(self.pair1, self.pair2)
        self.maxLeverage = maxLeverage
        # a dictionary of the complete feeds
        self._completeFeeds = {}
        # a dictionary of timeframe feeds
        self.feeds = {}
        # dictionary which lists all the open order 
        # dictionary of one trader to many order
        self.orders = defaultdict(OrderedDict)
        # dictionary which matches a trader to a position
        # positions are one trader ton one position
        self.positions = {}
        # dictionary cache which continuously snips feeds
        self.snipperCache = {}
    
    def limitBuy(
        self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
    ):
        NotImplemented

    def limitSell(
        self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
    ):
        NotImplemented

    def marketBuy(
        self, trader, quantity, leverage=1, reduceOnly=False
    ):
        NotImplemented

    def marketSell(
        self, trader, quantity, leverage=1, reduceOnly=False
    ):
        NotImplemented
    
    def stopMarketBuy(
        self, trader, stop, quantity, leverage=1, reduceOnly=False
    ):
        NotImplemented

    def stopMarketSell(
        self, trader, stop, quantity, leverage=1, reduceOnly=False
    ):
        NotImplemented

    def assignTo(self, exchange):
        self.exchange = exchange
        self.makerFee = exchange.makerFee
        self.takerFee = exchange.takerFee
    
    def addOrder(self, order):
        orderDictionary = self.orders[order.trader]
        orderid = len(orderDictionary)
        if orderid in orderDictionary.keys():
            while orderid in orderDictionary.keys():
                orderid += 1
        orderDictionary[orderid] = order
        order.id = orderid

    def getOrders(self, trader):
        return self.orders[trader]
    
    def availableFeeds(self):
        return [key for key in self._completeFeeds.keys()]
    
    def addFeed(self, feed):
        if len(self._completeFeeds) == 0:
            self.smallestTimeframe = feed.timeframe
        elif feed.timeDelta <= self._completeFeeds[self.smallestTimeframe].timeDelta:
            self.smallestTimeframe = feed.timeframe
        self._completeFeeds[feed.timeframe] = feed

    def getLatestClosePrice(self):
        return self.feeds[self.smallestTimeframe][:,-1][4]

    def getLatestOpenPrice(self):
        return self.feeds[self.smallestTimeframe][:,-1][1]

    def getLatestFeed(self):
        return self.feeds[self.smallestTimeframe][:,-1]

    def getLatestTime(self):
        return self.feeds[self.smallestTimeframe][:,-1][0]

    def getStartTime(self):
        return self._completeFeeds[self.smallestTimeframe].data[:,0][0]

    def __len__(self):
        return len(self._completeFeeds[self.smallestTimeframe])
    
    def __iter__(self):
        completeFeeds = [key for key in self._completeFeeds.keys()]
        for key in completeFeeds:
            self.snipperCache[key] = 0
        self.clippableKeys = [
            key for key in completeFeeds if key != self.smallestTimeframe
        ]

        self.counter = 0
        self._childFeeds = {key: self._completeFeeds[key] for key in self.clippableKeys}
        self._mainFeed = self._completeFeeds[self.smallestTimeframe]
        self._maxLen = len(self)
        return self
    
    def __next__(self):

        if self.counter > self._maxLen:
            raise StopIteration
        
        self.counter += 1

        mainfeedClipped = self._mainFeed.data[:, :self.counter]

        self.feeds[self.smallestTimeframe] = mainfeedClipped

        latestDate = mainfeedClipped[0, -1]

        for key in self.clippableKeys:
            dates = self._childFeeds[key].data[0, self.snipperCache[key]:]
            try:
                topDate = np.max(np.where(dates <= latestDate)) + self.snipperCache[key]
                self.feeds[key] = self._childFeeds[key].data[:, 0:topDate+1]
                self.snipperCache[key] = topDate
            except:
                self.feeds[key] = None

        # now check see whether a position is liquidated
        # [position.isLiquidated for position in self.positions.values()]
        # process all the orders 
        traderKeys = list(self.orders.keys())
        for key in traderKeys:
            orderKeys = list(self.orders[key].keys())
            for okey in orderKeys:
                self.orders[key][okey].process()
        # close zero positions

        return self.feeds

    def __repr__(self):
        return f"<market: {self.pair1}-{self.pair2} {self.availableFeeds()}>"


    
