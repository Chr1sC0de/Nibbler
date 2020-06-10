from uuid import uuid1
from collections import defaultdict
from abc import abstractmethod
import matplotlib.pyplot as plt

class Trader:

    def __init__(self, intialBalance=1000):
        self.id = str(uuid1())[0:6]
        self.balance = intialBalance
        # trade logging
        self.trades = []
        self.tradesWon = 0
        self.tradesLost = 0
        # win and loss %
        self.winPercentages = []
        self.lossPercentages = []
        # dictionary of buy and sells per market
        self.buyTimestamps = defaultdict(list) 
        self.sellTimestamps = defaultdict(list)
        # log the positions
        self.positions = dict()
        # log the orders
        self.orders = defaultdict(dict)

    def registerExchange(self, exchange):
        self.exchange = exchange

    def isLiquidated(self):
        if self.balance <= 0:
            return True
        return False

    def strategy(self):
        NotImplemented

    def __repr__(self):
        return f"<{self.id}: accountBalance={self.balance}>"
        
        