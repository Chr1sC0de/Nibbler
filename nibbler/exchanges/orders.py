import abc
from . exchange import Exchange, Account
from ..markets import Market


class Order(abc.ABC):

    side = None
    kind = None

    @classmethod
    def from_total_spent(
        cls,
        market : Market,
        account: Account,
        price  : float,
        total  : float
    ):
        amount = total/price
        return cls(market, account, price, amount)

    @abc.abstractclassmethod
    def check_already_triggered(cls, market, price):
        NotImplemented

    def __new__(cls,
        market         : Market,
        account        : Account,
        price          : float,
        amount         : float,
        timestop       : int = None,
        is_market_price: bool = False
    ):
        if cls.check_already_triggered(market, price):
            is_market_price = True
        return super().__new__(
            cls, market, account, price, amount,
            timestop, market, is_market_price
        )

    def __init__(
        self,
        market         : Market,
        account        : Account,
        price          : float,
        amount         : float,
        timestop       : int = None,
        is_market_price: bool = False
    ):
        assert market.kind == self.kind
        self.market          = market
        self.account         = account
        self.price           = price
        self.amount          = amount
        self.is_market_price = is_market_price
        self.id              = None
        self.vault           = 0
        self.set_timestop(timestop)

        self.initialize()
        self.add_self_to_market_and_account()

    def add_self_to_market_and_account(self):
        order_dict = self.market.orders[self.account]
        order_id = len(order_dict)
        while order_id in order_dict.keys():
            order_id += 1
        self.id = order_id
        order_dict[order_id] = self
        self.account.orders[self.market][order_id] = self

    def set_timestop(self, timestop):
        if timestop is not None:
            if timestop > self.market.currentdatetime:
                self.timestop = timestop
            else:
                raise Exception("Assigned timestop is in the past")
        else:
            self.timestop = None

    def is_timestopped(self):
        if self.timestop is not None:
            if self.market.current_datetime >= self.timestop:
                return True
        return False

    def process(self):
        if self.is_market_price:
            self.price = self.market.current_open
        elif self.check_triggered():
            self.on_fill()
            if self.vault == 0:
                self.close()
        elif self.is_timestopped():
            self.close()

    def close(self):
        self.return_vault()
        self.close_datetime = self.market.master_feed.current_datetime
        del self.market.orders[self.account][self.id]
        del self.account.orders[self.market][self.id]

    @abc.abstractmethod
    def check_triggered(self):
        NotImplemented

    @abc.abstractmethod
    def initialize(self):
        NotImplemented

    @abc.abstractmethod
    def on_fill(self):
        NotImplemented

    @abc.abstractmethod
    def return_vault(self):
        NotImplemented