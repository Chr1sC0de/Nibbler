from ... import binance as bf
import pandas as pd
import numpy as np
from collections import deque
from functools import wraps
from scipy.optimize import least_squares
# fees
maker = 0.0002
taker = 0.0004

def is_successful(function):
    @wraps(function)
    def wrapped(self, *args, **kwargs):
        try:
            result = function(self, *args, **kwargs)
            return result
        except:
            return None
    return wrapped

precisionDict = {
    "BTCUSDT": {"quantity":3, "price":2},
}

class TradingAgentBase(object):

    def __init__(
        self, *,
        api_key, secret_key,
        risk=0.005, symbol="BTCUSDT"
        ):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.risk = risk
        self.requester = bf.RequestClient(api_key=api_key, secret_key=secret_key)
        self.balance = self.get_balance()
        self.symbol = symbol

    @property
    def precision_price(self):
        return precisionDict[self.symbol]["price"]

    @property
    def precision_quantity(self):
        return precisionDict[self.symbol]["quantity"]

    def get_balance(self, key="USD"):
        balances = self.requester.get_balance()
        for balance in balances:
            if key in balance.asset:
                return balance.balance
        raise Exception(r"key {key} is not available")

    def get_order_book(self, limit=10):
        result = self.requester.get_order_book(
            symbol=self.symbol, limit=limit
        )
        return result

    def get_asks(self, limit=10):
        # ordered from smallest to highest
        asks = self.get_order_book(limit=limit).asks
        return pd.DataFrame(
            [[ask.price, ask.qty] for ask in asks],
            columns=["price", "qty"]
        )

    def get_bids(self, limit=10):
        # ordered from highest to smallest
        bids = self.get_order_book(limit=limit).bids
        return pd.DataFrame(
            [[bid.price, bid.qty] for bid in bids],
            columns=["price", "qty"]
        )

    #---------buy and sell orders

    @is_successful
    def post_buy_order(self, *, price, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.BUY,
            ordertype=bf.model.OrderType.LIMIT,
            timeInForce="GTX",
            quantity=quantity, price=price,
            **kwargs)
        return result

    @is_successful
    def post_sell_order(self, *, price, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.SELL,
            ordertype=bf.model.OrderType.LIMIT,
            timeInForce="GTX",
            quantity=quantity, price=price,
            **kwargs)
        return result

    @is_successful
    def post_sell_reduce_order(self, *, price, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.SELL,
            ordertype=bf.model.OrderType.LIMIT,
            timeInForce="GTX",
            reduceOnly=True,
            quantity=quantity, price=price,
            **kwargs)
        return result

    @is_successful
    def market_buy_order(self, *, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.BUY,
            ordertype=bf.model.OrderType.MARKET,
            timeInForce=bf.model.TimeInForce.INVALID,
            quantity=quantity,
            **kwargs)
        return result

    @is_successful
    def market_sell_order(self, *, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.SELL,
            ordertype=bf.model.OrderType.MARKET,
            timeInForce=bf.model.TimeInForce.INVALID,
            quantity=quantity,
            **kwargs)
        return result

    @is_successful
    def sell_stop_limit_order(self, *, stopPrice, price, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.SELL,
            ordertype=bf.model.OrderType.MARKET,
            timeInForce="GTX",
            quantity=quantity, price=price, stopPrice=stopPrice,
            **kwargs)
        return result

    @is_successful
    def sell_stop_market_order(self, *, stopPrice, quantity, **kwargs):
        result = self.requester.post_order(
            symbol=self.symbol, side=bf.model.OrderSide.SELL,
            ordertype=bf.model.OrderType.STOP_MARKET,
            timeInForce=bf.model.TimeInForce.INVALID,
            quantity=quantity, price=None,
            stopPrice=stopPrice,
            **kwargs)
        return result

    @is_successful
    def sell_stop_reduce_buy_market(self, *, stopPrice, quantity, **kwargs):
        result = self.sell_stop_market_order(
            stopPrice=stopPrice, quantity=quantity, reduceOnly=True, **kwargs)
        return result

    #---------positions

    def get_all_open_orders(self):
        result = self.requester.get_open_orders(symbol=self.symbol)
        return result

    def get_buy_orders(self):
        orders = self.get_all_open_orders()
        orders = [order for order in orders if "BUY" in order.side]
        orders.sort(key = lambda x:x.price)
        return orders

    def get_sell_orders(self):
        orders = self.get_all_open_orders()
        orders = [order for order in orders if "SELL" in order.side]
        orders.sort(key = lambda x:x.price)
        return orders

    def get_all_positions(self):
        positions = self.requester.get_position()
        return [position for position in positions if position.positionAmt > 0]

    def get_symbol_position(self):
        positions = self.get_all_positions()
        for position in positions:
            if self.symbol in position.symbol:
                return position
        return None

    #---------closing positions
    @is_successful
    def close_symbol_orders(self):
        result = self.requester.cancel_all_orders(symbol=self.symbol)
        return result

    @is_successful
    def close_order(self, orderId):
        result = self.requester.cancel_order(symbol=self.symbol, orderId=orderId)
        return result

    @is_successful
    def close_all_sell_limit_orders(self):
        sell_orders = self.get_sell_orders()
        for order in sell_orders:
            if "LIMIT" in order.origType:
                self.close_order(
                    order.orderId
                )

    @is_successful
    def close_all_buy_limit_orders(self):
        buy_orders = self.get_buy_orders()
        for order in buy_orders:
            if "LIMIT" in order.origType:
                self.close_order(
                    order.orderId
                )

    @is_successful
    def close_all_sell_stop_orders(self):
        sell_orders = self.get_sell_orders()
        for order in sell_orders:
            if "STOP" in order.origType:
                self.close_order(
                    order.orderId
                )



class TradingAgentSpecialEntries(TradingAgentBase):

    @is_successful
    def sell_scale_out_buy(
        self, *,
        quantity,
        meanPrice, priceDeviation,
        n_entries = 10, distribution=np.random.normal
    ):
        quantity_per_entry = quantity/n_entries
        quantity_per_entry = np.around(
            quantity_per_entry, decimals=self.precision_quantity)
        exits = distribution(meanPrice, priceDeviation, n_entries)
        exits.sort()
        exits = np.array(
            [np.around(price, decimals=self.precision_price)
                for price in exits]
        )
        for price in exits:
            self.post_sell_reduce_order(
                price=price, quantity=quantity_per_entry
            )
        leftover = quantity - (quantity_per_entry*n_entries)

        if leftover > 0:
            self.post_sell_order(
                price=meanPrice, quantity=leftover
            )


    @is_successful
    def risk_based_distributed_buy_entry(
        self, *,
        stopPrice, quantity,
        meanPrice, priceDeviation,
        n_entries=10,
        distribution=np.random.gumbel):
        # calculate the stop based off of the mean price and stop price
        entry_prices = distribution(meanPrice, priceDeviation, n_entries)
        entry_prices.sort()

        entry_prices = np.array(
            [np.around(price, decimals=self.precision_price)
                for price in entry_prices]
        )

        initial_guess = np.ones_like(entry_prices) * (quantity/n_entries)

        def residual(x):
            return sum((entry_prices-stopPrice)*x) - quantity*(meanPrice-stopPrice)

        solution = least_squares(
            residual, initial_guess,  bounds=(0, quantity),
            loss="soft_l1",ftol=1e-13, xtol=1e-13, gtol=1e-13,
            jac="3-point"
        )

        mirco_orders = solution.x
        mirco_orders = np.array(
            [np.around(order, decimals=self.precision_quantity)
                for order in mirco_orders]
        )

        solsum = mirco_orders.sum()

        # error = np.abs((quantity-solsum)/quantity*100)

        mirco_orders = mirco_orders-(quantity-solsum)/n_entries

        mirco_orders = np.array(
            [np.around(order, decimals=self.precision_quantity)
                for order in mirco_orders]
        )
        solsum = mirco_orders.sum()
        assert solsum <= quantity, \
            "quantity cannot be divided, try a different combination"

        all_orders = []

        for order, price in zip(mirco_orders, entry_prices):
            if order>0:
                order = self.post_buy_order(
                    price=price, quantity=order
                )

                all_orders.append(order)

        return all_orders

    @is_successful
    def protect_buy_orders(
        self, *,
        stopPrice,
        orderList):

        quantity = 0
        for order in orderList:
            quantity += order.origQty

        self.sell_stop_reduce_buy_market(
            stopPrice=stopPrice, quantity=quantity
        )
