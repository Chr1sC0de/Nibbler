from nibbler.optim import market, trade, exchange
from nibbler.signals.buy import SavitzkyMin
from nibbler.signals.sell import SavitzkyMax
import nibbler.plot as nplt
import pathlib as pt
import matplotlib.pyplot as plt
import talib
import ta
import pandas as pd
from tqdm import tqdm
import numpy as np
from bokeh.io import export_png
from bokeh import models
from collections import defaultdict


Mode = "b"
class MemoryMax(SavitzkyMax):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, mode=Mode, **kwargs)
        self.memory = defaultdict(list)
    
    def __call__(self, key, *args, **kwargs):
        self.key = key
        return super().__call__(*args, **kwargs)
    
    def process(self, desiredField):
        if len(self.features):
            latestFeature = self.features[-1]
            if latestFeature not in self.memory[self.key]:
                self.memory[self.key].append(latestFeature)
                self.memory[self.key] = self.memory[self.key][-self.signalRetain:]
                if latestFeature >= (len(desiredField) - 1 - self.signalRetain):
                    return True
        return False


class MemoryMin(SavitzkyMin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, mode=Mode, **kwargs)
        self.memory = defaultdict(list)
        
    def __call__(self, key, *args, **kwargs):
        self.key = key
        return super().__call__(*args, **kwargs)
    
    def process(self, desiredField):
        if len(self.features):
            latestFeature = self.features[-1]
            if latestFeature not in self.memory[self.key]:
                self.memory[self.key].append(latestFeature)
                self.memory[self.key] = self.memory[self.key][-self.signalRetain:]
                if latestFeature >= (len(desiredField) - 1 - self.signalRetain):
                    return True
        return False


class LongOnlyTrader(trade.Trader):

    '''
        self.balance(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        self.positions(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        self.orders(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        # For a market(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        limitBuy(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        limitSell(trader, quantity, entryPrice, leverage=1, reduceOnly=False)
        marketBuy(trader, quantity, leverage=1, reduceOnly=False)
        marketSell(trader, quantity, leverage=1, reduceOnly=False)
        stopMarketBuy(trader, quantity, stop, leverage=1, reduceOnly=False)
        stopMarketSel(trader, quantity, stop, leverage=1, reduceOnly=False)

    '''

    def __init__(
            self,
            signalWindow, gradientWindow,
            signalPoly=3, gradientPoly=3,
            clip=200, risk=0.01, atrFactor=2.5, signalRetain=30,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.minSignal = MemoryMin(
            signalWindow, gradientWindow,
            signalPoly=signalPoly, gradientPoly=gradientPoly,
            signalRetain=signalRetain, field="low"
        )
        self.maxSignal = MemoryMax(
            signalWindow, gradientWindow,
            signalPoly=signalPoly, gradientPoly=gradientPoly,
            signalRetain=signalRetain, field="high"
        )
        self.clip = clip
        self.risk = risk
        self.atrFactor = atrFactor
        self.balanceHistory = [list(), list()]
        self.wait = False

    def getBalanceHistory(self):
        return np.array(self.balanceHistory)

    def strategy(self):

        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds
        btc_1hr = btcFeeds["1h"]
        btc_4hr = btcFeeds["4h"]
        # btc_15m = btcFeeds["15m"]

        self.balanceHistory[0].append(market.getLatestTime())
        self.balanceHistory[1].append(self.balance)

        if len(btc_4hr[0]) > self.clip:

            if self.minSignal("4hr", btc_4hr):
                quantity, leverage, stop = self.calQuantityLeverageStop() 
                btcMarket.marketBuy(self, quantity, leverage)

            # if not self.wait:
            if self.positions:
                if self.maxSignal("4hr", btc_4hr):
                    position = self.positions[btcMarket]
                    quantity = position.quantity
                    leverage = position.leverage
                    btcMarket.marketSell(
                        self, quantity, leverage, reduceOnly=True)

                    

    def calQuantityLeverageStop(self):
        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds
        btc_4hr = btcFeeds["4h"]

        atr = talib.ATR(
            btc_4hr[2,-100:],
            btc_4hr[3,-100:],
            btc_4hr[4,-100:]
        )

        riskedAmount = self.balance * self.risk
        priceMovement = self.atrFactor*atr[-1]
        quantity = riskedAmount/priceMovement
        latestClosePrice = btcMarket.getLatestClosePrice()
        dollarAmount = quantity * latestClosePrice
        # now calculate the leverage
        leverage = dollarAmount/riskedAmount * 1.1
        if leverage > btcMarket.maxLeverage:
            leverage = int(btcMarket.maxLeverage) - 1
        # now calculate the stop price
        stop = latestClosePrice - priceMovement
        return quantity, leverage, stop



if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    resourceFolder = cwd/"../../../resources/csv"

    dataPath4hr = resourceFolder/"BitcoinBinance4hr.csv"
    dataPath1hr = resourceFolder/"BitcoinBinance1hr.csv"
    dataPath15m = resourceFolder/"BitcoinBinance15m.csv"
    # extract the data feeds here
    feed4hr = market.CSVFeed(dataPath4hr)
    feed1hr = market.CSVFeed(dataPath1hr)
    feed15m = market.CSVFeed(dataPath15m)
    # initialize a market, trader and an exchange
    market = market.Market("BTC", "USD")
    nwin = 77
    gradFilt = int(nwin*2)
    trader1 = LongOnlyTrader(
        nwin, gradFilt, signalPoly=3,
        gradientPoly=3, risk=0.01, clip=int(2.5*nwin),
        intialBalance=1000
    )
    # trader2 = LongOnlyTrader(21, 21)
    binance = exchange.Exchange("binance")
    # add timeframe feeds to the market
    market.addFeed(feed4hr)
    market.addFeed(feed1hr)
    market.addFeed(feed15m)
    # now add markets and traders to the exchange
    binance.addMarket(market)
    binance.addTrader(trader1)
    # binance.addTrader(trader2)
    # initialize the exchange
    binance.initialize()
    # now step forward into the market
    pbar = tqdm(total=len(market))
    counter = 0
    imageCounter = 0
    figures = []
    while binance.step():
        '''
            do some logging or visualization for the trader here
        '''
        pbar.update()
        if False:
            plt.plot(*trader1.getBalanceHistory(), label="big")
            # plt.plot(*trader2.getBalanceHistory(), label="small")
            plt.legend()
            plt.show()
        if False:
            if trader1.positions:

                if counter%1 == 0:

                    feed = market.feeds["1h"]
                    clippedFeed = feed[:, -1000:]

                    orders = trader1.orders[market]
                    position = trader1.positions[market]

                    ax = nplt.movie.candlesticks(clippedFeed)
                    ax = nplt.movie.position(clippedFeed, position, ax)

                    for order in orders.values():
                        ax = nplt.movie.order(clippedFeed, order, ax)

                    ax = nplt.movie.volume(clippedFeed, ax)

                    ax.spines["right"].set_color("none")
                    ax.spines["top"].set_color("none")

                    plt.gcf().savefig(
                        "movie/%07d.png"%imageCounter, dpi=75
                    )
                    plt.close()
                    imageCounter += 1

                if trader1.balance == 0:
                    ax = nplt.movie.candlesticks(clippedFeed)
                    ax = nplt.movie.volume(clippedFeed, ax)

                    ax.spines["right"].set_color("none")
                    ax.spines["top"].set_color("none")
                    plt.gcf().savefig(
                        "movie/%07d.png"%imageCounter, dpi=75
                    )
                    break

            counter += 1
        pass
    plt.plot(*trader1.getBalanceHistory())
    plt.show()
    pass