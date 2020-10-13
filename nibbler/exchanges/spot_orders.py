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
        if self.market.current_close <= self.price:
            return True
        return False

    def initialize(self):
        funds       = self.wallet_1.withdraw(self.amount)
        self.vault += funds
    
    def on_fill(self):
        # get the slippage from the market
        self.wallet_2.fund(self.vault/self.price) 

    def plot(self):
        pass