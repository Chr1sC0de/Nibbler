from ..market import Market
from .order import (
    LimitBuy, LimitSell,
    MarketBuy, MarketSell,
    StopMarketBuy, StopMarketSell
)


def limitBuy(
    self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
):
    LimitBuy(
        trader, self, quantity, entryPrice, 
        leverage=leverage, reduceOnly=reduceOnly
    )

def limitSell(
    self, trader, quantity, entryPrice, leverage=1, reduceOnly=False
):
    LimitSell(
        trader, self, quantity, entryPrice, 
        leverage=leverage, reduceOnly=reduceOnly
    )

def marketBuy(
    self, trader, quantity, leverage=1, reduceOnly=False
):
    MarketBuy(
        trader, self, quantity, leverage=leverage, reduceOnly=reduceOnly
    )

def marketSell(
    self, trader, quantity, leverage=1, reduceOnly=False
):
    MarketSell(
        trader, self, quantity, leverage=leverage, reduceOnly=reduceOnly
    )

def stopMarketBuy(
        self, trader, stop, quantity, leverage=1,
        reduceOnly=False, stopSlippage=0.0001
    ):
        StopMarketBuy(
            trader, self, stop, quantity,
            leverage=leverage, reduceOnly=reduceOnly,
            stopSlippage=stopSlippage
        )

def stopMarketSell(
        self, trader, stop, quantity, leverage=1, 
        reduceOnly=False, stopSlippage=0.0001
    ):
        StopMarketSell(
            trader, self, stop, quantity,
            leverage=leverage, reduceOnly=reduceOnly,
            stopSlippage=stopSlippage
        )
#---------------------------------------------------
Market.LimitBuy = limitBuy
Market.limitSell = limitSell
Market.marketBuy = marketBuy
Market.marketSell = marketSell
Market.stopMarketBuy = stopMarketBuy
Market.stopMarketSell = stopMarketSell