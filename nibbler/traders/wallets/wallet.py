import abc
import numpy as np


class Wallet(abc.ABC):

    _repr_decimals = 3

    @abc.abstractproperty
    def kind(self):
        return NotImplemented

    def __init__(self, asset, balance=0):

        self.asset   = asset
        self.balance = balance

        self._history = [self.balance, ]

    def log_balance(self):
        self._history.append(self.balance)

    @property
    def history(self):
        return np.array(self._history)

    def __repr__(self):
        template = \
            f"%sWallet asset=%s balance=%0.{self._repr_decimals}f"
        return template%(self.kind, self.asset, self.balance)


class Spot(Wallet):
    kind = "spot"

class Margin(Wallet):
    kind = "margin"

    def __init__(self, *args, **kwargs):
        self.borrowed       = 0
        self.collateralized = 0