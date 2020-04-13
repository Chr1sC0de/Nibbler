import numpy as np
import scipy.signal as ss
import scipy.interpolate as si
from ..math import make_odd

def min_finder_filtered_grads(data, window_length=12, poly_order=3):

    first_derivative = np.gradient(data)
    first_derivative = ss.savgol_filter(
        first_derivative, make_odd(window_length), poly_order,
    )

    t_0 = first_derivative[0:-1]
    t_1 = first_derivative[1:]

    le_0 = np.less_equal(t_0, 0)
    ge_1 = np.greater_equal(t_1, 0)

    mins = np.logical_and(
        ge_1, le_0
    )

    return mins


def max_finder_filtered_grads(data, window_length=12, poly_order=3):

    first_derivative = np.gradient(data)
    first_derivative = ss.savgol_filter(
        first_derivative, make_odd(window_length), poly_order,
    )

    t_0 = first_derivative[0:-1]
    t_1 = first_derivative[1:]

    ge_0 = np.greater_equal(t_0, 0)
    le_1 = np.less_equal(t_1, 0)

    maxes = np.logical_and(
        ge_0, le_1
    )

    return maxes

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