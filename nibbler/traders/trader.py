from collections import OrderedDict, defaultdict
from uuid import uuid1
from typing import List
import abc


class Trader:

    def __init__(
        self,
        exchange       = None,
        spotwallets    = None,
        marginwallets  = None,
        futuresbalance = None
    ):
        self.id       = str(uuid1())[0:10]
        if exchange is not None:
            self.register_to_exchange(exchange)
        else:
            self.exchange = None
        # initialize the wallet dictionaries
        self.spotwallets   = OrderedDict()
        self.marginwallets = OrderedDict()

        self.orders          = defaultdict(OrderedDict)
        self.positions       = defaultdict(OrderedDict)
        self.futures_balance = futuresbalance
        self.futures_history = []

    def log_futures(self):
        self.futures_history.append(self.futures_history)

    def fund_futures(self, amount):
        wallet = self.spotwallets["USDT"]
        if wallet.balance < amount:
            amount = wallet.balance
        wallet.balace        -= amount
        self.futures_balance += amount


    def register_to_exchange(self, exchange:"nibbler.exchanges.Exchange"):
        self.exchange = exchange
        exchange.addtraders(self)

    def addwallets(self, *wallets:List["nibbler.trader.wallets.Wallet"]):
        for wallet in wallets:
            if wallet.kind == "spot":
                self.spotwallets[wallet.asset] = wallet
            elif wallet.kind == "margin":
                self.marginwallets[wallet.asset] =  wallet

    @abc.abstractmethod
    def strategy(self):
        NotImplemented

    def addpositions(self, *positionList):
        for position in positionList:
            if position is not None:
                self.positions[position.market][position.id] = position

    def addorders(self, *orderList):
        for order in orderList:
            if order is not None:
                self.orders[order.market][order.id] = order

    def __repr__(self):
        return "<%s id:%s>"%(self.__class__.__name__, self.id)