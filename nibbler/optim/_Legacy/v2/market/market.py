from .feed import Feed
import numpy as np
from collections import defaultdict


class Market:

    timeframeDict = {
        1000*60:"m",
        1000*60*60:"h",
        1000*60*60*24:"d",
        1000*60*60*24*7:"w"
    }
    timeframeToSeconds = {
        "m": 1000*60,
        "h": 1000*60*60,
        "d": 1000*60*60*24,
        "w": 1000*60*60*24*7
    }

    def __init__(self, name: str, maxLeverage:float = 125):
        self.name = name
        self.maxLeverage = maxLeverage
        self._feeds = dict() 
        self.snipperCache = dict()
        self.feeds = dict()
        self.orders = {}
        self.positions = {}
    
    def addOrder(self, order):
        order.setID(len(self.orders))
        self.orders[len(self.orders)] = order
    
    def addPosition(self, position):
        position.setID(len(self.positions))
        self.positions[len(self.positions)] = position

    def startTime(self):
        return self._feeds[self.smallestTimeframe].start_time()
    
    def endTime(self):
        return self._feeds[self.smallestTimeframe].end_time()
    
    def setExchange(self, exchange):
        self.exchange = exchange

    def addFeed(self, feed:Feed):
        if len(self._feeds) == 0:
            self.smallestTimeframe = feed.timeframe
        elif feed.timeDelta <= self._feeds[self.smallestTimeframe].timeDelta:
            self.smallestTimeframe = feed.timeframe
        self._feeds[feed.timeframe] = feed

    def availableFeeds(self):
        return list(self._feeds.keys())

    def __len__(self):
        return len(self._feeds[self.smallestTimeframe])
    
    def __iter__(self):

        for key in self.availableFeeds():
            self.snipperCache[key] = 0

        self.clippableKeys = [
            key for key in self.availableFeeds() if key!=self.smallestTimeframe
        ]

        self.counter = 0
        self._childFeeds = {key: self._feeds[key] for key in self.clippableKeys}
        self._mainFeed = self._feeds[self.smallestTimeframe]
        self._maxLen = len(self)
        return self

    def __next__(self):
        
        if self.counter > self._maxLen:
            raise StopIteration
        
        self.counter += 1

        mainfeedClipped = self._mainFeed._data[:, :self.counter]

        self.feeds[self.smallestTimeframe] = mainfeedClipped

        latestDate = mainfeedClipped[0, -1]

        for key in self.clippableKeys:
            dates = self._childFeeds[key]._data[0, self.snipperCache[key]:]
            try:
                topDate = np.max(np.where(dates<=latestDate)) \
                    + self.snipperCache[key]
                self.feeds[key] = self._childFeeds[key]._data[
                    :, 0:topDate+1
                ]
                self.snipperCache[key] = topDate 
            except:
                self.feeds[key] = None
        
        # check all the orders,

        # check all he positions,
            
        return self.feeds
