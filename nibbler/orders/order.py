import abc
from .. import plt


class Side(str):
    pass


class sides:

    BUY  = Side("buy")
    SELL = Side("sell")


class Order(abc.ABC):

    side = None
    kind = None

    def __init__(
        self,
        market    : "nibbler.markets.Market",
        trader    : "nibbler.traders.Trader",
        quantity  : float,
        entryprice: float,
        timestop  : int = None,
        **kwargs
    ):
        assert market.kind == self.kind
        self.market     = market
        self.trader     = trader
        self.quantity   = quantity
        self.entryprice = entryprice
        self.settimestop(timestop)

        self.id       = None
        self.opendate = self.market.masterfeed.currentdatetime
        self.vault    = 0

        self.checkviable()
        self.initialize()
        self.market.addorders(self)
        self.trader.addorders(self)

        self.filled = False

    @abc.abstractmethod
    def checkviable(self, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def initialize(self, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def _get_fee_fraction(self):
        NotImplemented

    @abc.abstractmethod
    def _return_vault(self, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def _check_triggered(self):
        NotImplemented

    @abc.abstractmethod
    def _on_fill(self):
        NotImplemented

    def process(self):
        self.triggered = self._check_triggered()
        if self.triggered:
            self._on_fill()
            self.close()
            return 0
        self.checkviable()
        if self.is_timestopped():
            self.close()
        return 1

    def close(self):
        self._return_vault()
        self.closedatetime = self.market.masterfeed.currentdatetime
        del self.market.orders[self.trader][self.id]
        del self.trader.orders[self.market][self.id]

    def is_timestopped(self):
        if self.timestop is not None:
            if self.market.currentdatetime >= self.timestop:
                return True
        return False

    def settimestop(self, timestop):
        if timestop is not None:
            if timestop > self.market.currentdatetime:
                self.timestop = timestop
            else:
                raise Exception("Assigned timestop is in the past")
        else:
            self.timestop = None

    @property
    def traderwallets(self):
        return getattr(self.trader, f"{self.kind}wallets")

    @property
    def wallet1(self):
        # buy pair
        return self.traderwallets[self.market.pair1]

    @property
    def wallet2(self):
        # sell pair
        return self.traderwallets[self.market.pair2]

    def plot(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        return ax
