import numpy as np
import scipy.signal as ss
import scipy.interpolate as si
from ..math import make_odd

def min_finder_filtered_grads(data, window_length=12, poly_order=3):
    x = np.arange(len(data))
    splrep  = si.splrep(
        x, data
    )
    first_derivative = si.splev(x, splrep, der=1)
    second_derivative = si.splev(x, splrep, der=2)

    first_derivative = ss.savgol_filter(
        first_derivative, make_odd(window_length), poly_order,
    )

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

def max_finder_filtered_grads(data, window_length=12, poly_order=3):
    x = np.arange(len(data))
    splrep  = si.splrep(
        x, data
    )
    first_derivative = si.splev(x, splrep, der=1)
    second_derivative = si.splev(x, splrep, der=2)

    first_derivative = ss.savgol_filter(
        first_derivative, make_odd(window_length), poly_order,
    )

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


def min_open_filtered_grads(open, window_length=12, poly_order=3):
    return min_finder_filtered_grads(open, window_length=window_length, poly_order=poly_order)
def min_high_filtered_grads(high, window_length=12, poly_order=3):
    return min_finder_filtered_grads(high, window_length=window_length, poly_order=poly_order)
def min_low_filtered_grads(low, window_length=12, poly_order=3):
    return min_finder_filtered_grads(low, window_length=window_length, poly_order=poly_order)
def min_close_filtered_grads(close, window_length=12, poly_order=3):
    return min_finder_filtered_grads(close, window_length=window_length, poly_order=poly_order)

def max_open_filtered_grads(open, window_length=12, poly_order=3):
    return max_finder_filtered_grads(open, window_length=window_length, poly_order=poly_order)
def max_high_filtered_grads(high, window_length=12, poly_order=3):
    return max_finder_filtered_grads(high, window_length=window_length, poly_order=poly_order)
def max_low_filtered_grads(low, window_length=12, poly_order=3):
    return max_finder_filtered_grads(low, window_length=window_length, poly_order=poly_order)
def max_close_filtered_grads(close, window_length=12, poly_order=3):
    return max_finder_filtered_grads(close, window_length=window_length, poly_order=poly_order)