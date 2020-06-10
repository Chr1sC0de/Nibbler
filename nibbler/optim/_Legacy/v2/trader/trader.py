import uuid


class Trader:

    def __init__(self, initialBalance=1000):

        self.id = uuid.uuid1()

        self.openPositions = {} 
        self.closedPositions = {}

        self.balance = initialBalance

        self.isLiquidated = False
    