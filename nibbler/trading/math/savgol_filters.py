import scipy.signal as ss

def make_odd(value):
    value = int(value)
    if (value % 2) == 0:
        return value + 1
    else:
        return value

def savitzky_golay_open(
        open, window_length=12, polyorder=3,
        deriv=0, delta=1.0, mode='interp', cval=0):
    window_length = make_odd(window_length)
    return ss.savgol_filter(
        open, window_length, polyorder,
        deriv=deriv, delta=delta, mode='interp', cval=cval)


def savitzky_golay_high(
        high, window_length=12, polyorder=3,
        deriv=0, delta=1.0, mode='interp', cval=0):

    window_length = make_odd(window_length)
    return ss.savgol_filter(
        high, window_length, polyorder,
        deriv=deriv, delta=delta, mode='interp', cval=cval)


def savitzky_golay_low(
        low, window_length=12, polyorder=3,
        deriv=0, delta=1.0, mode='interp', cval=0):
    window_length = make_odd(window_length)
    return ss.savgol_filter(
        low, window_length, polyorder,
        deriv=deriv, delta=delta, mode='interp', cval=cval)


def savitzky_golay_close(
        close, window_length=12, polyorder=3,
        deriv=0, delta=1.0, mode='interp', cval=0):
    window_length = make_odd(window_length)
    return ss.savgol_filter(
        close, window_length, polyorder,
        deriv=deriv, delta=delta, mode='interp', cval=cval)