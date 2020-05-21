

class User:

    __slots__ = [
        "account_balance"
    ]

    def __init__(self, account_balance=1000):
        self.account_balance = account_balance