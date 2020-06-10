from uuid import uuid1
import abc
from ..market import LongPosition


class Order:

    def __init__(
            self, trader, market, quantity, value
        ):
        self.trader = trader 
        self.quantity = quantity
        self.value = value
        self.setMarket(market)

    def setID(self, id):
        self.id = id
    
    def setMarket(self, market):
        self.market = market 
        market.addOrder(self)
    
    def close(self):
        del self.market.orders[self.id]
    
    @abc.abstractmethod
    def process(self):
        NotImplemented
#-----------------------------------------
class LimitOrder(Order):
    def __init__(self, trader, market, quantity, value):
        super().__init__(trader, market, quantity, value)
        assert value != market.feeds[market.smallestTimeframe]

class LimitBuy(LimitOrder):
    def __init__(self, trader, market, quantity, value):
        super().__init__(trader, market, quantity, value)
        assert value < market.feeds[market.smallestTimeframe]

    def process(self):
        if self.market.feeds[self.market.lowestTimeframe][3,-1] < self.value:
            position = LongPosition(
                self.trader, self.market, self.quantity, self.value) 
            self.market.addPosition(position)
            self.close()


class LimitSell(LimitOrder):
    pass
#-----------------------------------------
class MarketOrder(Order):
    pass

class MarketBuy(Order):
    pass

class MarketSell(Order):
    pass
#-----------------------------------------
class StopOrder(Order):
    pass

class StopBuy(StopOrder):
    pass

class StopSell(StopOrder):
    pass