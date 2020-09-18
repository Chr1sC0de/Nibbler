from matplotlib import transforms
from . import Order, Stop, sides
from .. import plt


class Spot(Order):

    kind       = "spot"
    _linecolor = None
    _linestyle = "dashed"

    def plot(self, ax=None ,**kwargs):
        ax     = super().plot(ax=ax, **kwargs)
        string = str(self)
        ax.axhline(
            y         = self.entryprice,
            linestyle = self._linestyle,
            color     = self._linecolor
        )
        trans = transforms.blended_transform_factory(
            ax.transAxes, ax.transData)
        ax.text(
            0.5, 0.99*self.entryprice,
            s         = string,
            ha        = "center",
            transform = trans
        )
        return ax

    def __repr__(self):
        template = "<%s%sOrder quantity=%0.3f price=%0.3f vault=%0.3f>"
        return template%(
            self.kind.capitalize(),
            self.side.capitalize(),
            self.quantity,
            self.entryprice,
            self.vault
        )



class Buy(Spot):

    side       = sides.BUY
    _linecolor = "green"

    def initialize(self):
        amount_desired = self.quantity * self.entryprice
        assert self.wallet2.balance >= amount_desired, \
            "wallet balance is too low"
        self.wallet2.balance -= amount_desired
        self.vault           += amount_desired

    def checkviable(self):
        if self.entryprice > self.market.currentclose:
            self.entryprice = self.market.currentclose

    def _return_vault(self):
        self.wallet2.balance += self.vault
        self.vault            = 0

    def _on_fill(self):
        quantity_transferred = self.market.slippage(self.quantity)
        self.wallet1.balance += quantity_transferred * (1 - self._get_fee_fraction())
        self.vault -= quantity_transferred * self.entryprice


class Sell(Spot):

    side       = sides.SELL
    _linecolor = "red"

    def initialize(self):
        amount_desired = self.quantity
        assert self.wallet1.balance >= amount_desired, \
            "wallet balance is too low"
        self.wallet1.balance -= amount_desired
        self.vault           += amount_desired

    def checkviable(self):
        if self.entryprice < self.market.currentclose:
            self.entryprice = self.market.currentclose

    def _return_vault(self):
        self.wallet1.balance += self.vault
        self.vault            = 0

    def _on_fill(self):
        quantity_transferred = self.market.slippage(self.quantity)
        self.wallet2.balance += quantity_transferred * (
            1 - self._get_fee_fraction())*self.entryprice
        self.vault -= quantity_transferred
# ---------------------------------------------------------------------------- #
#                                     limit                                    #
# ---------------------------------------------------------------------------- #
class _limitbase:
    def _get_fee_fraction(self):
        return self.market.makerfee


class limit:


    class Buy(_limitbase, Buy):

        def _check_triggered(self):
            if self.market.currentlow < self.entryprice:
                return True
            return False


    class Sell(_limitbase, Sell):

        def _check_triggered(self):
            if self.market.currenthigh > self.entryprice:
                return True
            return False
# ---------------------------------------------------------------------------- #
#                                    market                                    #
# ---------------------------------------------------------------------------- #
class _marketbase:

    def __init__(
        self,
        market    : "nibbler.markets.Market",
        trader    : "nibbler.traders.Trader",
        quantity  : float,
        timestop  : int = None,
        **kwargs
    ):
        super().__init__(market, trader, quantity, None, timestop, **kwargs)

    def checkviable(self):
        self.entryprice = self.market.currentclose

    def _get_fee_fraction(self):
        return self.market.makerfee

    def _check_triggered(self):
        return True


class market:

    class Buy(_marketbase, Buy):
        pass

    class Sell(_marketbase, Sell):
        pass
# ---------------------------------------------------------------------------- #
#                                     stop                                     #
# ---------------------------------------------------------------------------- #

class _stopbase(Stop):
    kind = "spot"

class stop:

    class limit:

        class Buy(_stopbase):

            side = sides.BUY

            def place_order(self):
                limit.Buy(
                    self.market, self.trader, self.quantity, self.entryprice,
                    timestop=self.timestop
                )

        class Sell(_stopbase):

            side = sides.SELL

            def place_order(self):
                limit.Sell(
                    self.market, self.trader, self.quantity, self.entryprice,
                    timestop=self.timestop
                )

    class market:

        class Buy(Stop):

            side = sides.BUY

            def place_order(self):
                market.Buy(
                    self.market, self.trader, self.quantity, timestop=self.timestop
                )

        class Sell(Stop):

            side = sides.SELL

            def place_order(self):
                market.Sell(
                    self.market, self.trader, self.quantity, timestop=self.timestop
                )