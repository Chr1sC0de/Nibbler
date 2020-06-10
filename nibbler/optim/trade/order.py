from ..market import (
    LongPosition, ShortPosition, Market
)


class Order:

    orderType = "abstractBase"
    
    def __init__(
            self, trader, market, 
            quantity, entryPrice, leverage=1,
            reduceOnly=False
        ):
        self.reduceOnly = reduceOnly
        self.leverage = leverage
        self.trader = trader
        self.market = market
        self.quantity = quantity
        self.entryPrice = entryPrice
        self.id = None
        self.openDate = market.getLatestTime()
        market.addOrder(self)
        assert self.id is not None
        self.trader.orders[market][self.id] = self
    
    def close(self):
        del self.market.orders[self.trader][self.id]
        del self.trader.orders[self.market][self.id]

    def process(self):
        NotImplemented

    def getSmallestFeed(self):
        return self.market.feeds[self.market.smallestTimeframe]

    def __repr__(self):
        output = "<Order: trader=%s, market=%s-%s, entryPrice=%0.3f, quantity=%0.3f, type=%s>"
        return output%(
            self.trader.id,
            self.market.pair1,
            self.market.pair2,
            self.entryPrice,
            self.quantity,
            self.orderType
        )
#---------------------------------------------------
class LimitOrder(Order):

    def __init__(
            self, trader, market, quantity,
            entryPrice, leverage=1, reduceOnly=False
        ):
        super().__init__(
            trader, market, quantity, entryPrice,
            leverage=leverage, reduceOnly=reduceOnly
        )
        self.checkEntry()

    def checkEntry(self):
        NotImplemented


class LimitBuy(LimitOrder):

    orderType = "limitBuy"

    def checkEntry(self):
        reqFeed = self.getSmallestFeed()
        assert reqFeed[4, -1] > self.entryPrice

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]
        if reqFeed[3,-1] <= self.entryPrice:
            LongPosition(
                self.trader, self.market, self.quantity, 
                self.entryPrice, leverage=self.leverage, reduceOnly=self.reduceOnly
            )
            self.close()


class LimitSell(LimitOrder):

    orderType = "limitSell"

    def checkEntry(self):
        reqFeed = self.getSmallestFeed()
        assert reqFeed[4, -1] < self.entryPrice

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]
        if reqFeed[2,-1] >= self.entryPrice:
            ShortPosition(
                self.trader, self.market, self.quantity, 
                self.entryPrice, leverage=self.leverage, reduceOnly=self.reduceOnly
            )
            self.close()
#----------------------------------------------------
class MarketOrder(Order):
    orderType = "market"
    def __init__(
            self, trader, market, 
            quantity, leverage=1,
            reduceOnly=False
        ):
        super().__init__(
            trader, market, quantity, "market",
            leverage=leverage,
            reduceOnly=reduceOnly
        )

    def __repr__(self):
        output = "<Order: trader=%s, market=%s-%s, entryPrice=%s, quantity=%0.3f, type=%s"
        return output%(
            self.trader.id,
            self.market.pair1,
            self.market.pair2,
            self.entryPrice,
            self.quantity,
            self.orderType
        )

class MarketBuy(MarketOrder):
    orderType = "marketBuy"
    def process(self):
        LongPosition(
            self.trader, self.market, self.quantity, 
            self.entryPrice, leverage=self.leverage, reduceOnly=self.reduceOnly
        )
        self.close()


class MarketSell(MarketOrder):
    orderType = "marketSell"
    def process(self):
        ShortPosition(
            self.trader, self.market, self.quantity, self.entryPrice,
            leverage=self.leverage, reduceOnly=self.reduceOnly
        )
        self.close()

#----------------------------------------------------
class StopLimit(LimitOrder):
    def __init__(
            self, trader, market, stop, quantity,
            entryPrice, leverage=1, reduceOnly=False
        ):
        super().__init__(
            trader, market, quantity, entryPrice,
            leverage=leverage, reduceOnly=reduceOnly
        )
        self.stop = stop
        self.stopped = False

    def checkStopToEntry(self, stop, entryPrice):
        NotImplemented
    def checkEntry(self):
        NotImplemented


class StopLimitBuy(StopLimit):

    orderType = "stopLimitBuy"
    def checkEntry(self):
        pass
        # reqFeed = self.getSmallestFeed()
        # assert reqFeed[4, -1] < self.entryPrice

    def checkStopToEntry(self, stop, entryPrice):
        assert stop < self.getSmallestFeed()[3, -1]

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]
        if reqFeed[2,-1] >= self.stop:
            self.stopped = True
        if self.stopped:
            if reqFeed[2, -1] >= self.entryPrice:
                LongPosition(
                    self.trader, self.market, self.quantity, 
                    self.entryPrice, leverage=self.leverage,
                    reduceOnly=self.reduceOnly
                )
                self.close()

class StopLimitSell(StopLimit):

    orderType = "stopLimitSell"
    def checkEntry(self):
        pass
        # reqFeed = self.getSmallestFeed()
        # assert reqFeed[4, -1] < self.entryPrice

    def checkStopToEntry(self, stop, entryPrice):
        assert stop < self.getSmallestFeed()[3,-1]

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]
        if reqFeed[2,-1] >= self.stop:
            self.stopped = True
        if self.stopped:
            if reqFeed[2, -1] >= self.entryPrice:
                ShortPosition(
                    self.trader, self.market, self.quantity, 
                    self.entryPrice, leverage=self.leverage,
                    reduceOnly=self.reduceOnly
                )
                self.close()
#---------------------------------------------------
class StopMarket(MarketOrder):

    def __init__(
        self, trader, market, stop,
        quantity, leverage=1,
        reduceOnly=False, stopSlippage=0.0001
    ):
        self.checkStop(stop, market)
        super().__init__(
            trader, market, quantity,
            leverage=leverage,
            reduceOnly=reduceOnly
        )
        self.stopSlippage = stopSlippage
        self.stop = stop
        self.stopped = False

    def checkStop(self, stop, market):
        NotImplemented


class StopMarketBuy(StopMarket):

    orderType = "stopMarketBuy"
    def checkStop(self, stop, market):
        latestFeed = market.getLatestFeed()
        assert stop > latestFeed[4] 

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]
        if reqFeed[2,-1] >= self.stop:
            self.stopped = True
        if self.stopped:
            self.entryPrice = (1+self.stopSlippage) * self.stop
            LongPosition(
                self.trader, self.market, self.quantity, 
                self.entryPrice, leverage=self.leverage,
                reduceOnly=self.reduceOnly
            )
            self.close()

class StopMarketSell(StopMarket):

    orderType = "stopMarketSell"

    def checkStop(self, stop, market):
        latestFeed = market.getLatestFeed()
        assert stop < latestFeed[4] 

    def process(self):
        reqFeed = self.market.feeds[self.market.smallestTimeframe]

        if reqFeed[3,-1] <= self.stop:
            self.stopped = True
        if self.stopped:
            self.entryPrice = (1-self.stopSlippage) * self.stop
            ShortPosition(
                self.trader, self.market, self.quantity, 
                self.entryPrice, leverage=self.leverage,
                reduceOnly=self.reduceOnly
            )
            self.close()

#---------------------------------------------------

def limitBuy(
    self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
):
    LimitBuy(
        trader, self, quantity, entryPrice, 
        leverage=leverage, reduceOnly=reduceOnly
    )

def limitSell(
    self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
):
    LimitSell(
        trader, self, quantity, entryPrice, 
        leverage=leverage, reduceOnly=reduceOnly
    )

def marketBuy(
    self, trader, quantity, leverage=1, reduceOnly=False
):
    MarketBuy(
        trader, self, quantity, leverage=leverage, reduceOnly=reduceOnly
    )

def marketSell(
    self, trader, quantity, leverage=1, reduceOnly=False
):
    MarketSell(
        trader, self, quantity, leverage=leverage, reduceOnly=reduceOnly
    )

def stopMarketBuy(
        self, trader, stop, quantity, leverage=1,
        reduceOnly=False, stopSlippage=0.0001
    ):
        StopMarketBuy(
            trader, self, stop, quantity,
            leverage=leverage, reduceOnly=reduceOnly,
            stopSlippage=stopSlippage
        )

def stopMarketSell(
        self, trader, stop, quantity, leverage=1, 
        reduceOnly=False, stopSlippage=0.0001
    ):
        StopMarketSell(
            trader, self, stop, quantity,
            leverage=leverage, reduceOnly=reduceOnly,
            stopSlippage=stopSlippage
        )
#---------------------------------------------------
Market.limitBuy = limitBuy
Market.limitSell = limitSell
Market.marketBuy = marketBuy
Market.marketSell = marketSell
Market.stopMarketBuy = stopMarketBuy
Market.stopMarketSell = stopMarketSell