from . import Market


class Spot(Market):

    kind = "spot"
    makerfee = 0.001
    takerfee = 0.001