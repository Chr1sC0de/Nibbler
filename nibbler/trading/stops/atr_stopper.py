import talib
import numpy as np
def atr_stopper(trading_env, data):

    atr_values = talib.ATR(
        np.array(data['open']), 
        np.array(data['high']),
        np.array(data['low']),
        14
    )

    stop = data.close.iloc[-1] - atr_values[-1]*2.5
    return stop