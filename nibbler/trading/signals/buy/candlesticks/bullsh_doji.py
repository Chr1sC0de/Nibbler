from .base import Candlestick
import numpy as np
import talib
class Doji(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLDOJI(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class DragonflyDoji(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLDRAGONFLYDOJI(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()