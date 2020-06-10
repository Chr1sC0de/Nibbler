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
            atrFactor=1,
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
        self.longMode = False
        self.shortMode = False

    def getBalanceHistory(self):
        return np.array(self.balanceHistory)

    def strategy(self):

        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds

        btc_15m = btcFeeds["15m"]
        btc_1h = btcFeeds["1h"]
        btc_4h = btcFeeds["4h"]

        self.balanceHistory[0].append(market.getLatestTime())
        self.balanceHistory[1].append(self.balance)

        # get the emas for the 15m, 1h, 4h
        ema_15m_1, ema_15m_2, ema_15m_3 = self.getEMAs(btc_15m)
        ema_1h_1, ema_1h_2, ema_1h_3 = self.getEMAs(btc_1h)
        ema_4h_1, ema_4h_2, ema_4h_3 = self.getEMAs(btc_4h)

        if len(btc_1h[4]) > self.clip:

            # close all the orders if there are no positions
            if not self.positions:
                self.closeAllOrder()

            if all(
                [
                    self.checkCrossover(ema_4h_1, ema_4h_2, ema_4h_3),
                ]
            ):
                if all([
                    self.checkCrossover(ema_1h_1, ema_1h_2, ema_1h_3),
                    self.checkCrossover(ema_15m_1, ema_15m_2, ema_15m_3),
                    self.priceAboveEma(btc_1h, ema_1h_1, ema_1h_2, ema_1h_3),
                    self.priceAboveEma(btc_15m, ema_15m_1, ema_15m_2, ema_15m_3),
                    self.volumeIncreasing(btc_4h),
                    self.volumeIncreasing(btc_1h),
                    self.volumeIncreasing(btc_15m)
                ]):
                    atrFeed = self.getATR("1h")
                    quantity, entry, leverage, stop, target =\
                        self.getQantityLeverageStop(atrFeed[-1])
                    if leverage < btcMarket.maxLeverage:
                        # btcMarket.limitBuy(
                        #     self, quantity, entry, leverage=leverage, reduceOnly=False)
                        btcMarket.marketBuy(
                            self, quantity, leverage=leverage, reduceOnly=False
                        )
                        btcMarket.stopMarketSell(
                            self,  stop,quantity, leverage=leverage, reduceOnly=True)
                        btcMarket.limitSell(
                            self, quantity, target, leverage=leverage, reduceOnly=True)
                        self.longMode = True
                        self.shortMode = False

            if self.positions:
                position = self.positions[btcMarket]
                entry = position.entryPrice
                quantity = position.quantity
                leverage = position.leverage
                atr15m = self.getATR("15m")[-1]
                atr1h = self.getATR("1h")[-1]

                stop = entry - self.atrFactor*atr15m
                target = entry + self.atrFactor*atr1h*1.1

                try:
                    btcMarket.limitSell(
                        self, quantity, target, leverage=leverage, reduceOnly=True)
                except:
                    pass

                try:
                    if market.getLatestClosePrice() > (entry + 0.5*atr1h):
                        self.closeStops()
                        btcMarket.stopMarketSell(
                                self,  market.getLatestClosePrice()-atr1h,
                                quantity, leverage=leverage, reduceOnly=True)
                except:
                    pass
                    btcMarket.marketSell(
                        self, quantity, leverage=leverage, reduceOnly=True
                    )



    def getQantityLeverageStop(self, atr):

        btcMarket = self.exchange.markets["BTC-USD"]
        latestPrice = btcMarket.getLatestClosePrice()

        riskedAmmount = self.balance * self.risk
        priceMovement = self.atrFactor * atr

        entryPrice = latestPrice - priceMovement
        target = latestPrice + priceMovement*1.5
        stop = entryPrice - priceMovement

        fractionPriceMovement = 1-stop/entryPrice
        quantity = riskedAmmount/fractionPriceMovement/entryPrice
        leverage = quantity * entryPrice / riskedAmmount

        return quantity, entryPrice, leverage, stop, target

    def getEMAs(self, feed, *args):
        closes = feed[4][-self.clip:]
        if len(args)==0:
            return (
                talib.EMA(closes, self.ema1),
                talib.EMA(closes, self.ema2),
                talib.EMA(closes, self.ema3),
            )
        else:
            return (
                talib.EMA(closes, args[0]),
                talib.EMA(closes, args[1]),
                talib.EMA(closes, args[2]),
            )

    def checkCrossover(self, ema1, ema2, ema3):
        return all(
            [
                ema1[-1] > ema2[-1],
                ema1[-1] > ema3[-1],
                ema2[-1] > ema3[-1],
            ]
        )

    def checkSellCrossover(self, ema1, ema2, ema3):
        return all(
            [
                ema1[-1] < ema2[-1],
                ema1[-1] < ema3[-1],
                ema2[-1] < ema3[-1],
            ]
        )

    def volumeIncreasing(self, feed):
        volume =  feed[5]
        return all([
            volume[-1] > volume[-2],
            volume[-1] > volume[-3],
            volume[-1] > volume[-4],
            volume[-2] > volume[-3]
        ])

    def priceAboveEma(self, feed, ema1, ema2, ema3):
        _,dopen,_,_,close,_ = feed
        return all([
            dopen[-1] > ema1[-1],
            close[-1] > ema1[-1]
        ])

    def priceBellowEma(self, feed, ema1, ema2, ema3):
        _,dopen,_,_,close,_ = feed
        return all([
            dopen[-1] < ema1[-1],
            close[-1] < ema1[-1]
        ])

    def closeAllPositions(self):
        if self.positions:
            positionMarkets = list(self.positions.keys())
            for key in positionMarkets:
                self.positions[key].marketClose()

    def closeAllOrder(self):
        btcMarket = self.exchange.markets["BTC-USD"]
        if self.orders:
            orderByMarket = self.orders[btcMarket]
            orderkeys = list(orderByMarket.keys())
            for order in orderkeys:
                orderByMarket[order].close()

    def closeStops(self):
        btcMarket = self.exchange.markets["BTC-USD"]
        orders = self.orders[btcMarket]
        orderKeys = list(orders.keys())
        for key in orderKeys:
            order = orders[key]
            if isinstance( order, trade.StopMarketSell):
                order.close()

    def closeLimits(self):
        btcMarket = self.exchange.markets["BTC-USD"]
        orders = self.orders[btcMarket]
        orderKeys = list(orders.keys())
        for key in orderKeys:
            order = orders[key]
            if isinstance( order, trade.LimitSell):
                order.close()
    def getATR(self, key):
        btcMarket = self.exchange.markets["BTC-USD"]
        btcFeeds = btcMarket.feeds
        atr = talib.ATR(
                btcFeeds[key][2,-self.clip:],
                btcFeeds[key][3,-self.clip:],
                btcFeeds[key][4,-self.clip:]
            )
        return atr


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
        risk=0.02, clip=100,
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
                        cwd/("movie/%07d.png"%imageCounter), dpi=50
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
    plt.xlabel("datetime")
    plt.ylabel("equity")
    plt.show()
    print(trader1.tradesWon)
    print(trader1.tradesLost)
    print(np.mean(trader1.winPercentages))
    print(np.mean(trader1.lossPercentages))
    pass