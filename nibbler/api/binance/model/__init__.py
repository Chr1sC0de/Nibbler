from nibbler.api.binance.model.constant import *
from nibbler.api.binance.model.message import Msg
from nibbler.api.binance.model.exchangeinformation import ExchangeInformation
from nibbler.api.binance.model.orderbook import OrderBook
from nibbler.api.binance.model.trade import Trade
from nibbler.api.binance.model.aggregatetrade import AggregateTrade
from nibbler.api.binance.model.candlestick import Candlestick
from nibbler.api.binance.model.markprice import MarkPrice
from nibbler.api.binance.model.openinterest import OpenInterest
from nibbler.api.binance.model.fundingrate import FundingRate
from nibbler.api.binance.model.tickerpricechangestatistics import TickerPriceChangeStatistics
from nibbler.api.binance.model.symbolprice import SymbolPrice
from nibbler.api.binance.model.symbolorderbook import SymbolOrderBook
from nibbler.api.binance.model.liquidationorder import LiquidationOrder
from nibbler.api.binance.model.aggregatetradeevent import AggregateTradeEvent
from nibbler.api.binance.model.markpriceevent import MarkPriceEvent
from nibbler.api.binance.model.candlestickevent import CandlestickEvent
from nibbler.api.binance.model.symbolminitickerevent import SymbolMiniTickerEvent
from nibbler.api.binance.model.symboltickerevent import SymbolTickerEvent
from nibbler.api.binance.model.symbolbooktickerevent import SymbolBookTickerEvent
from nibbler.api.binance.model.liquidationorderevent import LiquidationOrderEvent
from nibbler.api.binance.model.orderbookevent import OrderBookEvent
from nibbler.api.binance.model.diffdepthevent import DiffDepthEvent
from nibbler.api.binance.model.order import Order
from nibbler.api.binance.model.balance import Balance
from nibbler.api.binance.model.accountinformation import AccountInformation
from nibbler.api.binance.model.leverage import Leverage
from nibbler.api.binance.model.changemargintype import ChangeMarginType
from nibbler.api.binance.model.positionmargin import PositionMargin
from nibbler.api.binance.model.positionmarginhistory import PositionMarginHist
from nibbler.api.binance.model.position import Position
from nibbler.api.binance.model.mytrade import MyTrade
from nibbler.api.binance.model.income import Income
from nibbler.api.binance.model.accountupdate import AccountUpdate
from nibbler.api.binance.model.orderupdate import OrderUpdate
from nibbler.api.binance.model.listenkeyexpired import ListenKeyExpired


reprable = [
    Msg, ExchangeInformation, Candlestick, MarkPrice, OpenInterest,
    FundingRate, TickerPriceChangeStatistics, SymbolPrice, SymbolOrderBook,
    LiquidationOrder, AggregateTradeEvent, MarkPriceEvent, CandlestickEvent,
    SymbolMiniTickerEvent, LiquidationOrderEvent, OrderBookEvent, DiffDepthEvent,
    Order, Balance, AccountInformation, Leverage, ChangeMarginType, PositionMargin,
    PositionMarginHist, Position, MyTrade, AccountUpdate, OrderUpdate, ListenKeyExpired
]

def customRepr(self):

    keys = [key for key in self.__dict__ if not key.startswith("__")]

    output_string  = [f"<{self.__class__.__name__}>"]
    output_string.extend(
        [f"|-----{key}: {self.__dict__[key]}" for key in keys]
    )
    return "\n".join(output_string)


for method in reprable:
    setattr(method, "__repr__", customRepr)
