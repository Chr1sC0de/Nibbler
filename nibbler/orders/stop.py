import abc
from matplotlib import transforms
from .. import plt


class Stop(abc.ABC):

    kind       = None
    side       = None
    _linestyle = "--"
    _linecolor = "k"

    def __init__(
        self,
        market    : "nibbler.markets.Market",
        trader    : "nibbler.traders.Trader",
        quantity  : float,
        entryprice: float,
        stop      : float,
        timestop  : int=None,
        **kwargs
    ):
        assert market.kind == self.kind
        self.market     = market
        self.trader     = trader
        self.quantity   = quantity
        self.entryprice = entryprice
        self.stop       = stop
        self.timestop   = timestop
        self.id         = None
        assert any(
            [
                stop > market.currentclose,
                stop < market.currentclose
            ]
        ), "stop should not equal the curent close"
        if stop < market.currentclose:
            self.mode = "less than"
            self.is_stopped = self.less_than
        if stop > market.currentclose:
            self.mode = "greater than"
            self.is_stopped = self.greater_than
        # now register the stop to the market
        market.addstops(self)

    @abc.abstractmethod
    def place_order(self):
        NotImplemented

    def process(self):
        if self.is_stopped():
            self.place_order()
            self.close()
            return 0
        return 1

    def less_than(self):
        if self.market.currentlow <= self.stop:
            return True
        return False

    def greater_than(self):
        if self.market.currenthigh >= self.stop:
            return True
        return False

    def close(self):
        del self.market.stops[self.trader][self.id]

    def plot(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()

        string = str(self)

        ax.axhline(
            y         = self.stop,
            linestyle = self._linestyle,
            color     = self._linecolor
        )

        trans = transforms.blended_transform_factory(
            ax.transAxes, ax.transData)

        ax.text(
            0.5, 0.99*self.stop,
            s         = string,
            ha        = "center",
            transform = trans
        )
        return ax

    def __repr__(self):
        template = "<%s%sStop %s %0.3f entry=%0.3f>"
        return template%(
            self.kind, self.side.capitalize(), self.mode, self.stop, self.entryprice
        )