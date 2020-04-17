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
    
class ThreeStarsInTheSouth(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDL3STARSINSOUTH(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class ThreeWhiteSoldiers(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDL3WHITESOLDIERS(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class Engulfing(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLENGULFING(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class MorningStar(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLMORNINGSTAR(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class EveningStar(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLEVENINGSTAR(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class EveningDojiStar(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLEVENINGDOJISTAR(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class MorningDojiStar(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLMORNINGDOJISTAR(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()