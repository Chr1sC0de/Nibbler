from nibbler.optim import market, trade, exchange
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
            clip=200, risk=0.01, 
            atrFactor=2.5,
            signalRetain=30,
            ema1=8, ema2=13, ema3=21,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.clip = clip
        self.risk = risk
        self.atrFactor = atrFactor
        self.balanceHistory = [list(), list()]
        self.ema1 = ema1
        self.ema2 = ema2
        self.ema3 = ema3

    def getBalanceHistory(self):
        return np.array(self.balanceHistory)
        
    def getEMAs(self, feed):
        closes = feed[4][-self.clip:]
        return (
            talib.EMA(closes, self.ema1),
            talib.EMA(closes, self.ema2),
            talib.EMA(closes, self.ema3),
        )


    def strategy(self):

        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds

        btc_15m = btcFeeds["15m"]
        btc_1hr = btcFeeds["1h"]
        btc_4hr = btcFeeds["4h"]

        self.balanceHistory[0].append(market.getLatestTime())
        self.balanceHistory[1].append(self.balance)

        if len(btc_1hr[4] > self.clip):

            # close all the orders if there are
            if not self.positions:
                if self.orders:
                    orderByMarket = self.orders[btcMarket]
                    orderkeys = list(orderByMarket.keys())
                    for order in orderkeys:
                        orderByMarket[order].close()


            closeData = btc_1hr[4][-self.clip:]
            openData = btc_1hr[1][-self.clip:]
            volumeData = btc_1hr[5][-self.clip:]

            ema1 = talib.EMA(closeData, self.ema1)
            ema2 = talib.EMA(closeData, self.ema2)
            ema3 = talib.EMA(closeData, self.ema3)

            self.currentEMAs = [ema1, ema2, ema3]

            # get the 4hr crossovers:

            closeData4hr  = btc_4hr[4][-self.clip:]
            openData4hr   = btc_4hr[1][-self.clip:]
            volumeData4hr = btc_4hr[5][-self.clip:]

            ema1_4hr = talib.EMA(closeData4hr, 21)
            ema2_4hr = talib.EMA(closeData4hr, 34)
            ema3_4hr = talib.EMA(closeData4hr, 55)

            if all(
                [
                    ema1_4hr[-1] > ema2_4hr[-1],
                    ema1_4hr[-1] > ema3_4hr[-1],
                    ema2_4hr[-1] > ema3_4hr[-1]
                ]
            ):

                if all(
                    [
                        ema1[-1] > ema2[-1],
                        ema1[-1] > ema3[-1],
                        ema2[-1] > ema3[-1]
                    ]
                ):
                    if all([
                        closeData[-1] > ema3[-1], openData[-1] > ema3[-1],
                        closeData[-1] > ema1[-1], openData[-1] > ema2[-1],
                    ]):
                        if all(
                            [
                                volumeData[-1] > volumeData[-2],
                                volumeData[-1] > volumeData[-3],
                                volumeData[-2] > volumeData[-3]
                            ]
                        ):

                            quantity, leverage, stop, atr = self.calculateLeverageAndStop()
                            currentPrice = btcMarket.getLatestClosePrice() 
                            target =  currentPrice + 1.5*self.atrFactor*atr

                            btcMarket.marketBuy(self, quantity, leverage)
                            btcMarket.limitSell(
                                self,
                                quantity,
                                target,
                                leverage,
                                reduceOnly=True,
                            )
                            btcMarket.stopMarketSell(
                                self, stop, quantity, leverage, reduceOnly=True)
                # else:
                #     if self.positions:
                #         self.positions[btcMarket].marketClose()
            else:
                if self.positions:
                    self.positions[btcMarket].marketClose()

            if self.positions:
                currentPrice = btcMarket.getLatestClosePrice() 
                entryPrice = self.positions[btcMarket].entryPrice
                quantity = self.positions[btcMarket].quantity
                leverage = self.positions[btcMarket].leverage
                atr = talib.ATR(
                    btcFeeds["15m"][2,-100:],
                    btcFeeds["15m"][3,-100:],
                    btcFeeds["15m"][4,-100:]
                )[-1]
                if currentPrice > (entryPrice + 2*atr):
                    # now change the stops 
                    orderkeys = list(self.orders[btcMarket].keys())
                    for order in orderkeys:
                        order = self.orders[btcMarket][order]
                        if isinstance( order, trade.StopMarketSell):
                            order.close()
                    btcMarket.stopMarketSell(
                            self, entryPrice + 0.5*atr, quantity, leverage, reduceOnly=True)
                     


    def calculateLeverageAndStop(self):
        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds
        btc_4hr = btcFeeds["1h"]

        atr = talib.ATR(
            btc_4hr[2,-100:],
            btc_4hr[3,-100:],
            btc_4hr[4,-100:]
        )[-1]

        riskedAmount = self.balance * self.risk
        priceMovement = self.atrFactor*atr
        quantity = riskedAmount/priceMovement
        latestClosePrice = btcMarket.getLatestClosePrice()
        dollarAmount = quantity * latestClosePrice
        # now calculate the leverage
        leverage = dollarAmount/riskedAmount * 1.1
        if leverage > btcMarket.maxLeverage:
            leverage = int(btcMarket.maxLeverage) - 1
        # now calculate the stop price
        stop = latestClosePrice - priceMovement
        return quantity, leverage, stop, atr


if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    resourceFolder = cwd/"../../../../../resources/csv"

    dataPath4hr = resourceFolder/"BitcoinBinance4hr.csv"
    dataPath1hr = resourceFolder/"BitcoinBinance1hr.csv"
    dataPath15m = resourceFolder/"BitcoinBinance15m.csv"
    # extract the data feeds here
    feed4hr = market.CSVFeed(dataPath4hr)
    feed1hr = market.CSVFeed(dataPath1hr)
    feed15m = market.CSVFeed(dataPath15m)
    # initialize a market, trader and an exchange
    market = market.Market("BTC", "USD")
    trader1 = LongOnlyTrader(
        risk=0.01, clip=100,
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
                        cwd/("movie/%07d.png"%imageCounter), dpi=75
                    )
                    plt.close()
                    imageCounter += 1

                if trader1.balance == 0:
                    ax = nplt.movie.candlesticks(clippedFeed)
                    ax = nplt.movie.volume(clippedFeed, ax)

                    ax.spines["right"].set_color("none")
                    ax.spines["top"].set_color("none")
                    plt.gcf().savefig(
                        cwd/("movie/%07d.png"%imageCounter), dpi=75
                    )
                    break

            counter += 1
        pass
    plt.plot(*trader1.getBalanceHistory())
    plt.show()
    pass