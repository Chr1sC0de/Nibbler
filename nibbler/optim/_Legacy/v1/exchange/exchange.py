from collections import Iterable
from ..user import User


class Exchange:

    __slots__ = [
        "user", "pairs"
    ]


    def __init__(self, user, pairs):

        assert isinstance(pairs, Iterable)
        assert issubclass(user.__class__, User)

        self.user = user
        self.pairs = pairs


    def run(self):
        pass




