from .orders import Order
from ..markets import Market
from . import SpotWallet, Account, Wallet
import abc


class SpotOrder(Order):

    @property
    def wallet_1(self) -> Wallet:
        return self.account.spot_wallets[self.market.pair1]

    @property
    def wallet_2(self)-> Wallet:
        return self.account.spot_wallets[self.market.pair2]
# ---------------------------------------------------------------------------- #
class SpotBuyOrder(SpotOrder):

    @classmethod
    def check_already_triggered(cls, market: Market, price: float):
        # when entering a buy order the buy order price must be less than or equal to
        # the current price, if it is greater than the current price then the order
        # is converted into a market order
        if price < market.current_close:
            return False
        return True

    def check_triggered(self):
        if self.market.current_low <= self.price:
            return True
        return False

    def initialize(self):
        self.vault += self.wallet_1.withdraw(self.amount)

    def on_fill(self):
        # get the slippage from the market
        intended_amount  = self.vault/self.price
        amount_filled    = self.market.fill_amount(intended_amount)
        amount_filled    = self.vault * slippage
        self.vault      -= amount_filled
        self.wallet_2.fund(amount_filled/self.price)

    def return_vault(self):
        self.wallet_1.fund(self.vault)
        self.vault = 0

    def plot(self):
        pass
# ---------------------------------------------------------------------------- #
class SpotSellOrder(SpotOrder):

    @classmethod
    def check_already_triggered(cls, market: Market, price: float):
        if price > market.current_close:
            return False
        return True

    def check_triggered(self):
        if self.market.current_high >= self.price:
            return True
        return False

    def initialize(self):
        self.vault += self.wallet_2.withdraw(self.amount)
    
    def on_fill(self):
        slippage = self.market.get_slippage()
        amount_filled = 


