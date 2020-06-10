from ..trader import Trader
from ..market import Market
import numpy as np
import abc
from uuid import uuid1

class Position(abc.ABC):


    def __init__(
            self, 
            trader: Trader,
            market: Market,
            quantity:float,
            value: float,
            leverage: float = 1
        ):
        # set the trader, market and leverage
        self.trader = trader
        self.market = market
        self.leverage = leverage
        # calculate the total cost to the trader 
        total = quantity * value
        position = total/leverage
        fee = market.exchange.makerFee * total
        # check that the trader can afford to make the trade
        assert fee + position <= self.trader.balance, "liquidated"
        # take the fee from the traders account
        self.trader.balance -= (fee + position)
        # log the quantity and open prices 
        self.quantity = quantity
        self.open = value 
        # create placeholders
        self.close = None
        self.won = False
        self.isopen = True

    @abc.abstractmethod
    def isLiquidated(self):
        NotImplemented

    @abc.abstractmethod
    def reduce(self, quantity:float, value: float):
        NotImplemented
    
    @abc.abstractmethod
    def reduceAll(self):
        NotImplemented


class LongPosition(Position):
    def isLiquidated(self):
        pass
    def reduce(self, quantity, value):
        pass
    def reduceAll(self):
        pass


class ShortPosition(Position):
    def isLiquidated(self):
        pass
    def reduce(self, quantity, value):
        pass
    def reduceAll(self):
        pass
