from collections import defaultdict, OrderedDict
from typing import List
import abc
from uuid import uuid1
from ..markets import Market
from  .. import markets as mk


class Wallet(abc.ABC):

    repr_decimals = 3

    def __init__(self, asset_name: str):
        """Base class for asset wallets

        Args:
            asset_name (str): name of asset i.e. "BTCUSDT", will be automatically
            capitalize.
        """
        self.asset   = asset_name.upper()
        self.balance = 0

    @abc.abstractproperty
    def kind(self):
        return NotImplmented

    def fund(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        assert amount <= self.balance, "insufficient funds"
        self.balance -= amount
        return amount

    def __repr__(self):
        template = \
            f"%sWallet asset=%s balance=%0.{self.repr_decimals}f"
        return template%(self.kind, self.asset, self.balance)


class SpotWallet(Wallet):
    kind = "spot"


class FuturesWallet(Wallet):
    kind = "futures"

    def __init__(self, asset_name: str):
        self.entry_price = None
        self.leverage    = None
        super().__init__(asset_name)

    def set_entry_price(
        self, amount: float, entry_price: float
    ):
        if self.entry_price is None:
            self.entry_price = entry_price
        else:
            self.entry_price = (
                self.entry_price * self.balance +
                entry_price * amount
            )/(self.balance + amount)
    
    def set_leverage(self, amount: float, leverage: float):
        if self.leverage == None:
            self.leverage = leverage
        else:
            self.leverage = (
                self.leverage * self.balance +
                leverage * amount
            )/(self.balance + amount)
        
    def fund(
        self, amount, entry_price, leverage
    ):
        if self.balance == 0:
            self.entry_price = None
            self.leverage    = None
        self.set_entry_price(amount, entry_price) 
        self.set_leverage(amount, leverage) 
        self.balance += amount

    def is_liquidated(self):
        return False


class FuturesUSDTWallet(Wallet):
    kind = "futures"

    def __init__(self):
        super().__init__("USDT")

    def fund(self, amount):
        self.balance += amount

    def is_liquidated(self):
        return False


class Account:

    def __init__(self, exchange: "Exchange"):
        """Base class for a user account

        Args:
            exchange (Exchange): Exchange which is linked to the user account
        """
        self.id              = str(uuid1())[0:10]
        self.exchange        = exchange
        self.orders          = defaultdict(OrderedDict)
        self.spot_wallets    = defaultdict(OrderedDict)
        self.futures_wallets = defaultdict(OrderedDict)

        self.spot_wallets   ["USDT"] = SpotWallet("USDT")
        self.futures_wallets["USDT"] = FuturesUSDTWallet()

    def transfer_spot_to_futures(self, amount):
        self.futures_wallets["USDT"].fund(self.spot_wallets["USDT"].withdraw(amount))

    def transfer_futures_to_spot(self, amount):
        self.spot_wallets["USDT"].fund(self.futures_wallets["USDT"].withdraw(amount))

    def __repr__(self):
        return "<%s id:%s>"%(self.__class__.__name__, self.id)


class Exchange:

    spot_maker_fee = 0.001
    spot_taker_fee = 0.001

    futures_maker_fee = 0.0002
    futures_taker_fee = 0.0004

    def __init__(self, name: str):
        """Exchange class

        Args:
            name (str):  name of exchange
        """
        self.name            = name
        self.spot_markets    = OrderedDict()
        self.futures_markets = OrderedDict()
        self.accounts        = OrderedDict()
        self._master_market  = None

    def new_account(self):
        account = Account(self)
        self.accounts[account.id] = account
        self.register_wallets_to_all_available_accounts()
        return account

    def new_spot_market(self, pair_1: str, pair_2: str) -> mk.Spot:
        new_market = mk.Spot(pair_1, pair_2, maker_fee=self.spot_maker_fee, taker_fee=self.spot_taker_fee)
        self.add_markets(new_market)
        return new_market

    def new_futures_market(self, pair_1: str, pair_2: str) -> mk.Futures:
        new_market = mk.Futures(pair_1, pair_2, maker_fee=self.futures_maker_fee, taker_fee=self.futures_taker_fee)
        self.add_markets(new_market)
        return new_market

    def add_markets(self, *markets: Market):
        for market in markets:
            if market.kind == "spot":
                self.spot_markets[market.name] = market
            elif market.kind == "futures":
                self.spot_markets[market.name] = market
            else:
                raise Exception("Unknown kind of market")
            if self._master_market is None:
                self._master_market =market
            elif market.start_datetime < self._master_market.start_datetime:
                self._master_market = market

    def get_all_markets(self) -> List[Market]:
        output = []
        [output.append(market) for market in self.spot_markets.values()]
        [output.append(market) for market in self.futures_markets.values()]
        return output

    def register_wallets_to_account(self, account: Account):
        for market in self.get_all_markets():
            market_kind = market.kind
            for market in self.get_all_markets():
                if market_kind == "spot":
                    for pair in [market.pair1, market.pair2]:
                        if pair not in account.spot_wallets.keys():
                            account.spot_wallets[pair] = SpotWallet(pair)

    def register_wallets_to_all_available_accounts(self):
        for account in self.accounts.values():
            self.register_wallets_to_account(account)

    def initialize(self):
        return iter(self)

    def step(self):
        return next(self)

    def __iter__(self):
        all_markets = self.get_all_markets()
        [market.set_master(self._master_market) for market in all_markets if
            market != self._master_market]
        [market.initialize() for market in all_markets]
        # process the futures wallets
        return self

    def __next__(self):
        self._master_market.step()
        return self

    def __repr__(self):
        return f"<{self.name}{self.__class__.__name__}>"