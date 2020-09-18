from collections import defaultdict, OrderedDict
from ..traders import wallets


class Exchange:

    def __init__(
        self, name
    ):
        self.name           = name
        self.spotmarkets    = OrderedDict()
        self.marginmarkets  = OrderedDict()
        self.futuresmarkets = OrderedDict()
        self.traders        = OrderedDict()
        self._mastermarket  = None

    def addtraders(self, *traders):
        for trader in traders:
            self.traders[trader.id] = trader

    def addmarkets(self, *markets):
        for market in markets:
            if market.kind is None:
                raise Exception("unknown kind of market")
            if market.kind == "spot":
                self.spotmarkets[market.name]    = market
            if market.kind == "margin":
                self.marginmarkets[market.name]  = market
            if market.kind == "futures":
                self.futuresmarkets[market.name] = market
            if self._mastermarket is not None:
                if market.startdatetime < self._mastermarket.startdatetime:
                    self._mastermarket = market
            else:
                self._mastermarket = market

    def getallmarkets(self):
        output = []
        [output.append(market) for market in self.spotmarkets.values()]
        [output.append(market) for market in self.marginmarkets.values()]
        [output.append(market) for market in self.futuresmarkets.values()]
        return output

    def register_available_assets_to_trader(self, trader: "nibbler.traders.Trader"):
        for market in self.getallmarkets():
            marketkind = market.kind
            if any([marketkind == "spot", marketkind == "margin"]):
                walletdict    = getattr(trader, f"{marketkind}wallets")
                walletbuilder = getattr(wallets, marketkind.capitalize())
                for pair in [market.pair1, market.pair2]:
                    if pair not in walletdict.keys():
                        walletdict[pair] = walletbuilder(
                            pair, balance=0)

    def initialize(self):
        return iter(self)

    def step(self):
        return next(self)

    def __iter__(self):
        allmarkets = self.getallmarkets()
        [market.setmaster(self._mastermarket) for
            market in allmarkets if market != self._mastermarket]
        [market.initialize() for market in allmarkets]
        for trader in self.traders.values():
            self.register_available_assets_to_trader(trader)
        return self

    def __next__(self):
        self._mastermarket.step()
        # now run the strategy for each trader
        for trader in self.traders.values():
            trader.strategy()

        return self

    def __repr__(self):
        return f"<{self.name}{self.__class__.__name__}>"