from .exchange import Exchange
from ..markets import Market, Spot, Futures
import abc


class TradingInterface(abc.ABC):

    def __init__(self, market_name: str, exchange: Exchange, account: Exchange.Account):
        self.exchange = exchange
        self.account  = account
        self.market   = self.get_market(market_name)
        assert account.id in exchange.accounts.keys(), \
            "trading account not registered to exchange"

    @abc.abstractmethod
    def get_market(self, market_name:str) -> Market:
        NotImplemented

    @abc.abstractmethod
    def limit_buy(self, price, amount, *args, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def limit_sell(self, price, amount, *args, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def market_buy(self, amount, *args, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def market_self(self, amount, *args, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def stop_limit_buy(self, amount, *args, **kwargs):
        NotImplemented

    @abc.abstractmethod
    def stop_limit_sell(self, amount, *args, **kwargs):
        NotImplemented


class SpotTrading(TradingInterface):

    def get_market(self, market_name:str) -> Spot:
        assert market_name in self.exchange.spot_markets.keys(), \
            f"{market_name} is not a spot market"
        return self.exchange.spot_markets[market_name]