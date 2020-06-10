class Exchange:

    def __init__(self, name, makerFee=0.001, takerFee=0.001):
        self.name = name
        self.makerFee = makerFee
        self.takerFee = takerFee
        self._markets = dict()
        self.markets = dict()
        self.traders = dict() 
        self.earliestMarket = 10000000000000000000000
        self.initilized = False
    
    def addTrader(self, trader):
        trader.registerExchange(self)
        self.traders[trader.id] = trader

    def addMarket(self, market):
        self._markets[market.name] = market
        market.makerFee = self.makerFee
        market.takerFee = self.takerFee
        for marketKey in self._markets.keys():
            if self._markets[marketKey].getStartTime() < self.earliestMarket:
                self.earliestMarket = marketKey

    def getStartTime(self):
        return self._markets[self.earliestMarket].getStartTime()
    
    def getActiveMarketsKeys(self):
        return [key for key in self.markets.keys()]
    
    def getLatestTime(self):
        return self.markets[self.earliestMarket].getLatestTime()
    
    def _maxIter(self):
        return len(self.markets[self.earliestMarket])

    def initialize(self):
        self.unusedMarkets = dict()

        for marketKey in self._markets.keys():
            if self._markets[marketKey].getStartTime() <= self.getStartTime():
                self.markets[marketKey] = self._markets[marketKey]

        for marketKey in self._markets.keys():
            if marketKey not in self.markets.keys():
                self.unusedMarkets[marketKey] = self._markets[marketKey]

        for marketKey in self.markets.keys():
            self.markets[marketKey] = iter(self.markets[marketKey])
        
        self.maxIter = self._maxIter()
        self.counter = 0
        self.initilized = True

    def step(self):

        assert self.initilized, "Exchange must be initialized"

        self.counter += 1
        # iterate all the markets
        if self.counter <= self.maxIter:
            [next(market) for market in self.markets.values()]
        else:
            print("Max steps in the market reached")
            return False
        # check whether or not the unused markets are running
        if self.unusedMarkets:
            unusedKeys = list(self.unusedMarkets.keys())
            for key in unusedKeys:
                if self.unusedMarkets[key].getStartTime() >= self.getLatestTime():
                    self.markets[key] = iter(self.unusedMarkets[key])
                    del self.unusedMarkets[unusedKeys]
        # for each trader check whether they have been liquidated
        traderKeys = list(self.traders.keys())
        for key in traderKeys:
            # negativeMovement = 0
            trader = self.traders[key]
            positionKeys = list(trader.positions.keys())
            for positionKey in positionKeys:
                trader.positions[positionKey].isLiquidated()
            # for position in trader.positions.values():
            #     negativeMovement += position.getLargestNegativePositionVariation()
            # if negativeMovement > trader.balance:
            #     trader.balance = 0
            #     del self.traders[key]
        # now we can implement the trader strategies
        [trader.strategy() for trader in self.traders.values()]
        # check to see if a trader is liquidated
        traders = list(self.traders.values())
        for trader in traders:
            if trader.balance <= 0:
                del self.traders[trader.id]
        return True