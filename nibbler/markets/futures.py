from collections import defaultdict, OrderedDict
import abc
from . import Market

class Futures(Market):

    kind     = "futures"
    makerfee = 0.0002
    takerfee = 0.0004

    class Position:

        def __new__(
            cls,
            market,
            trader,
            quantity,
            entryprice,
            timestop   = None,
            leverage   = 1,
            postonly   = False,
            reduceonly = False
        ):
            assert leverage <= market.maxleverage
            if trader in market.positons.keys():
                position = cls.modify_position(
                    market, quantity, trader, entryprice,
                    timestop=timestop, leverage=leverage, postonly=postonly,
                    reduceonly=reduceonly)
            elif not reduceonly:
                position = cls.newposition(
                    market, trader, quantity, entryprice,
                    timestop=timestop, leverage=leverage, postonly=postonly,
                    reduceonly=reduceonly
                )
            else:
                position = None

            return position

        @staticmethod
        def weightedaverage(p1, p2, w1, w2):
            return ((p1*w1)+(p2*w2))/(w1+w2)

        @staticmethod
        def get_entryprice(entryprice, market):
            if entryprice is market:
                entryprice = market.currentclose()
            return entryprice

        def close(self):
            del self.market.positions[self.trader]
            del self.trader.positions[self.market]

        def is_liquidated(self):
            if self.leverage == 1:
                return False
            dollar_movement = \
                self.get_largest_negative_variation() * self.quantity
            if dollar_movement >= self.get_margin():
                self.close()
                return True
            return False

        @classmethod
        def newposition(
            cls,
            market,
            trader,
            quantity,
            entryprice,
            timestop=None,
            leverage=1,
            postonly=False,
            reduceonly=False
        ):
            position            = object.__new__(cls)
            position.trader     = trader
            position.market     = market
            position.qunatity   = quantity
            position.leverage   = leverage
            position.entryprice = cls.get_entryprice(entryprice, market)

            dollar_cost = quantity * entryprice
            fees        = dollar_cost * self.get_fees()
            usercost    = dollar_cost/leverage * fees

            if usercost > trader.futures_balance:
                return None

            trader.futures_balance -= usercost
            market.positions[trader] = position
            trader.positions[market] = position

            return position


    def __init__(
        self, *args, funding_rate=None, maxleverage=75, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if funding_rate is None:
            self._funding_rate = lambda x: 0.0002
        else:
            self._funding_rate = funding_rate

        self.positions   = defaultdict(OrderedDict)
        self.maxleverage = maxleverage
