from .orders import Order
from ..markets import Market
from . import SpotWallet, Account
import abc


class SpotOrder(Order):

    @property
    def wallet_1(self):
        return self.account.spot_wallets[self.market.pair1]

    @property
    def wallet_2(self):
        return self.account.spot_wallets[self.market.pair2]


class SpotBuyOrder(SpotOrder):

    def initialize(self):
        funds       = self.wallet_1.withdraw(self.amount)
        self.vault += funds

    def check_viable(self):
        # when entering a buy order the buy order price must be less than or equal to
        # the current price, if it is greater than the current price then the order
        # is converted into a market order

    def plot(self):
        pass