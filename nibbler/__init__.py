from . import trading
from . import plot
from . import optim
from . import api

import numpy

def save(path, obj):
    numpy.save(path, obj)

def load(path):
    return numpy.load(path, allow_pickle=True).item()
