from ..market import Market
from ..trader import Trader
import re


class Exchange:

    def __init__(self, makerFee:float = 0.001, takerFee:float = 0.001):

        self.makerFee = makerFee
        self.takerFee = takerFee
        self.traders = {} 
        self._market = {}

        self.initialized = False
    
    def takeOrder(self, order, marketname):
        self.markets[marketname].addOrder(order)
    
    def availableMarkets(self):
        return [name for name in self.markets.keys()]
    
    def addMarket(self, market: Market):
        market.setExchange(self)
        self._market[market.name] = market

    def addTrader(self, trader:Trader):
        self.traders[trader.id] = trader

    def initialize(self):
        self.initialized = True
        newestMarket = None
        earliestTime = 10000000000000000000000

        [iter(self._market[key]) for key in self._market.keys()]
        
        for key, market in self._market.items():
            smallestTimeframe = market.smallestTimeframe
            multiplier = re.match("[0-9]+", smallestTimeframe)[0]
            timeframe = smallestTimeframe[len(multiplier):]
            multiplier = int(multiplier)

            if multiplier*market.timeframeToSeconds[timeframe] < earliestTime:
                newestMarket = key

        self.startTime = self._market[newestMarket].startTime()

        self.markets = {}

        for key in self._market.keys():
            if self._market[key].startTime() <= self.startTime:
                self.markets[key] = iter(self._market[key])

    def latestTime(self):
        key = next(iter(self._market.keys()))
        return self.markets[key][0][-1]

    def step(self):
        assert self.initialized, "before stepping forward the exchange must be initialized"

        for key in [key for key in self._market.keys() if key not in self.markets.keys()]:
            if self._market[key].startTime >= self.latestTime():
                self.markets[key] = self._market[key]
        
        for key in self.markets.keys():
            next(self.markets[key])

