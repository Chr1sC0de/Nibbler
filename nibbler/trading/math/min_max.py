import numpy as np
import scipy.signal as ss
import scipy.interpolate as si
from ..math import make_odd

def min_finder(data):
    x = np.arange(len(data))
    splrep  = si.splrep(
        x, data
    )
    first_derivative = si.splev(x, splrep, der=1)
    second_derivative = si.splev(x, splrep, der=2)

    mins_or_saddle = np.zeros_like(x)
    t_0 = first_derivative[0:-1]
    t_1 = first_derivative[1:]
    le_0 = np.less_equal(t_0, 0)
    ge_1 = np.greater_equal(t_1,0)
    mins_or_saddle[1:] = np.logical_and(
        ge_1, le_0
    )

    pos_or_ng = np.zeros_like(x)
    # if a min then the acceleration mus be positive
    pos_or_ng[second_derivative>0] = 1

    return np.logical_and(
        mins_or_saddle, pos_or_ng
    )

def max_finder(data):
    x = np.arange(len(data))
    splrep  = si.splrep(
        x, data
    )
    first_derivative = si.splev(x, splrep, der=1)
    second_derivative = si.splev(x, splrep, der=2)

    max_or_saddle = np.zeros_like(x)
    t_0 = first_derivative[0:-1]
    t_1 = first_derivative[1:]
    ge_0 = np.greater_equal(t_0, 0)
    le_1 = np.less_equal(t_1,0)
    max_or_saddle[1:] = np.logical_and(
        ge_0, le_1
    )

    pos_or_ng = np.zeros_like(x)
    # if a min then the acceleration mus be positive
    pos_or_ng[second_derivative<0] = 1

    return np.logical_and(
        max_or_saddle, pos_or_ng
    )

def min_finder_filtered(data, window_length=12, polyorder=3):
    window_length = make_odd(window_length)
    data = ss.savgol_filter(
        data, window_length=window_length, polyorder=polyorder,
    )
    return min_finder(data)

def max_finder_filtered(data, window_length=12, polyorder=3):
    window_length = make_odd(window_length)
    data = ss.savgol_filter(
        data, window_length=window_length, polyorder=polyorder,
    )
    return max_finder(data)

def min_open(open, window_length=12, polyorder=3):
    return min_finder_filtered(open, window_length=window_length, polyorder=polyorder)
def min_high(high, window_length=12, polyorder=3):
    return min_finder_filtered(high, window_length=window_length, polyorder=polyorder)
def min_low(low, window_length=12, polyorder=3):
    return min_finder_filtered(low, window_length=window_length, polyorder=polyorder)
def min_close(close, window_length=12, polyorder=3):
    return min_finder_filtered(close, window_length=window_length, polyorder=polyorder)

def max_open(open, window_length=12, polyorder=3):
    return max_finder_filtered(open, window_length=window_length, polyorder=polyorder)
def max_high(high, window_length=12, polyorder=3):
    return max_finder_filtered(high, window_length=window_length, polyorder=polyorder)
def max_low(low, window_length=12, polyorder=3):
    return max_finder_filtered(low, window_length=window_length, polyorder=polyorder)
def max_close(close, window_length=12, polyorder=3):
    return max_finder_filtered(close, window_length=window_length, polyorder=polyorder)