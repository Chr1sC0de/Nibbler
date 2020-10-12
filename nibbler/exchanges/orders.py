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

    def __init__(
        self,
        market  : Market,
        account : Account,
        price   : float,
        amount  : float,
        timestop: int = None
    ):
        assert market.kind == self.kind
        self.market  = market
        self.account = account
        self.price   = price
        self.amount  = amount
        self.id      = None
        self.set_timestop(timestop)

        self.check_viable()
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
        if self.check_triggered():
            self.on_fill()
            self.close()
            return 0
        self.check_viable()

    def close(self):
        self.return_vault()
        self.close_datetime = self.market.master_feed.current_datetime
        del self.market.orders[self.account][self.id]
        del self.account.orders[self.market][self.id]

    @abc.abstractmethod
    def check_viable(self):
        NotImplemented

    @abc.abstractmethod
    def initialize(self):
        NotImplemented

    @abc.abstractmethod
    def on_fill(self):
        NotImplemented

    @abc.abstractmethod
    def check_triggered(self):
        NotImplemented

    @abc.abstractmethod
    def return_vault(self):
        NotImplemented


class BuyOrder(Order):
    side = "buy"

    def initialize(self):
        pass
    

class SellOrder(Order):
    side = "sell"
