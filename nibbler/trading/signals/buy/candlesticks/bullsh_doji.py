from .base import Candlestick
import numpy as np
import talib
from nibbler.trading.math import max_finder, min_finder

class Doji(Candlestick):

    def candlestickmethod(self, dataframe):
        return np.argwhere(
            np.array(
                talib.CDLDOJI(dataframe['open'], dataframe['high'], dataframe['low'], dataframe['close'])
            )
        ).squeeze()

class DojiVWAP(Doji):

    def generate_features(self, dataframe):
        original_length = len(dataframe)

        if len(dataframe) > 500:
            dataframe = dataframe.loc[-500:]
        else:
            pass

        difference = original_length - len(dataframe)

        filtered_low = self.indicators[0](dataframe)
        filtered_high = self.indicators[1](dataframe)

        maxes = np.argwhere(max_finder(filtered_high)).squeeze()
        lows = np.argwhere(min_finder(filtered_low)).squeeze()

        typical_price = (dataframe["close"].values + dataframe["high"].values + dataframe["low"].values)/3
        volume_scaled_typical_price = typical_price * dataframe["volume"].values
        cum_vstp = np.cumsum(volume_scaled_typical_price)
        cum_vol = np.cumsum(dataframe["volume"].values)
        
        vwap =cum_vstp/cum_vol

        features = self.candlestickmethod(dataframe)

        if lows[-1] > maxes[-1]:
            if features.size:
                if features.size == 1:
                    if dataframe["low"][features] < vwap[features]:
                        return [int(features)+difference,]
                    else:
                        return []
                else:
                    if dataframe["low"][features[-1]] < vwap[features[-1]]:
                        return [features[-1]+difference,]
                    else:
                        return []
            else:
                return [ ]
        else:
            return [ ]



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