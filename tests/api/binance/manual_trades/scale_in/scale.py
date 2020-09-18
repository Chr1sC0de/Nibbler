import myconfig as mc
import click
import numpy as np
import logging
from binance.client import Client

precisions = {}

precisions["futures"] = {
    "ADAUSDT"  : {"price": 5, "quantity": 0 },
    "ALGOUSDT" : {"price": 4, "quantity": 2 },
    "BANDUSDT" : {"price": 4, "quantity": 1 },
    "BATUSDT"  : {"price": 3, "quantity": 1 },
    "BCHUSDT"  : {"price": 2, "quantity": 3 },
    "BLZUSDT"  : {"price": 5, "quantity": 1 },
    "BZRXUSDT" : {"price": 5, "quantity": 3 },
    "CRVUSDT"  : {"price": 3, "quantity": 1 },
    "DOTUSDT"  : {"price": 3, "quantity": 1 },
    "LENDUSDT" : {"price": 4, "quantity": 1 },
    "LINKUSDT" : {"price": 3, "quantity": 2 },
    "MATICUSDT": {"price": 5, "quantity": 1 },
    "MKRUSDT"  : {"price": 2, "quantity": 3 },
    "OMGUSDT"  : {"price": 4, "quantity": 1 },
    "SXPUSDT"  : {"price": 4, "quantity": 1 },
    "SUSHIUSDT": {"price": 4, "quantity": 1 },
    "WAVESUSDT": {"price": 4, "quantity": 1 },
    "XRPUSDT"  : {"price": 4, "quantity": 1 },
}

precisions["spot"] = {
    "ADAUSDT"  : {"price": 5, "quantity": 0 },
    "ALGOUSDT" : {"price": 4, "quantity": 2 },
    "BANDUSDT" : {"price": 4, "quantity": 1 },
    "BATUSDT"  : {"price": 3, "quantity": 1 },
    "BCHUSDT"  : {"price": 2, "quantity": 3 },
    "BLZUSDT"  : {"price": 5, "quantity": 1 },
    "BZRXUSDT" : {"price": 4, "quantity": 2 },
    "CRVUSDT"  : {"price": 3, "quantity": 1 },
    "DOTUSDT"  : {"price": 3, "quantity": 1 },
    "LENDUSDT" : {"price": 4, "quantity": 1 },
    "LINKUSDT" : {"price": 3, "quantity": 2 },
    "MATICUSDT": {"price": 5, "quantity": 1 },
    "MKRUSDT"  : {"price": 2, "quantity": 3 },
    "OMGUSDT"  : {"price": 4, "quantity": 1 },
    "SXPUSDT"  : {"price": 3, "quantity": 1 },
    "SUSHIUSDT": {"price": 3, "quantity": 3 },
    "WAVESUSDT": {"price": 4, "quantity": 1 },
    "XRPUSDT"  : {"price": 4, "quantity": 1 },
}

def read_pairs(input_string):
    return [float(item) for item in input_string.split(" ")]

def read_balances(input_string):
    if " " in input_string:
        return [float(item) for item in input_string.split(" ")]
    else:
        return [float(input_string), ]

def get_regions(all_levels):
    output = []
    for i in range(len(all_levels)-1):
        output.append(
            (all_levels[i], all_levels[i+1])
        )
    return output

class Distributions:
    @classmethod
    def linear(cls, upper_bound, lower_bound, n_levels, balance):
        order_levels = np.linspace(
            upper_bound, lower_bound, n_levels)
        balance_per_level = balance/n_levels
        return order_levels, balance_per_level

@click.command()
@click.option(
    "--pair",
    type=str,
    help="pair to trade"
)
@click.option(
    "--bounds",
    type=read_pairs,
    help="amount to trade"
)
@click.option(
    "--balances",
    type=read_balances,
    help="amount to trade"
)
@click.option(
    "--n_levels",
    type=int,
    help="total number of levels to enter"
)
@click.option(
    "--noise",
    default=True,
    type=bool,
    help="add some noise to your orders"
)
@click.option(
    "--futures",
    default=False,
    type=bool,
    help="use either futures or spot"
)
@click.option(
    "--close_orders" ,
    default=True,
    type=bool,
    help="close current order or not")
@click.option(
    "--distribution",
    default="linear",
    type=str,
    help="which distribution to use"
)
def main(
        pair, bounds, balances, n_levels, noise,
        futures, close_orders, distribution
    ):

    if futures:
        platform = "futures"
    else:
        platform = "spot"

    assert pair in precisions[platform].keys(), f"{pair} was not found in market keys"

    client        = Client(mc.api_key, mc.secret_key)
    assert bounds[0] > bounds[1]

    if len(balances) > 2:
        bounds = np.linspace(*bounds, len(balances)+1)
        bounds = get_regions(bounds)
    else:
        bounds = [bounds]

    all_actual_totals = []

    if close_orders:
        client.futures_cancel_all_open_orders(
            symbol=pair
        )

    for (upper, lower), balance in zip(bounds, balances):

        order_levels      = np.linspace(upper, lower, n_levels)
        balance_per_level = balance/n_levels

        price_precision    = precisions[platform][pair]["price"]
        quantity_precision = precisions[platform][pair]["quantity"]
        price_template     = f"%1.{price_precision}f"

        actual_total = 0


        for level in order_levels:

            quantity = balance_per_level/level

            if noise:
                perturbation = np.random.normal(0, 0.005, 1)[0]
                quantity *= (1 + perturbation)

            quantity = np.around(quantity, quantity_precision)
            level    = np.around(level, price_precision)

            if not futures:
                order    = client.order_limit_buy(
                    symbol   = pair,
                    quantity = quantity,
                    price    = price_template%level
                )
            else:
                order = client.futures_create_order(
                    symbol       = pair,
                    quantity     = quantity,
                    price        = price_template%level,
                    type         = "LIMIT",
                    side         = "BUY",
                    # positionSide = "LONG",
                    timeInForce  = "GTC",
                    leverage     = 1,
                    postOnly     = True
                )

            actual_total += level * quantity

        all_actual_totals.append(actual_total)

        print(
            (
                "Pair            : %s\n"+
                "Number of Levels: %s\n"+
                "Intended Balance: %0.5f\n"+
                "Actual Balance  : %0.5f\n"+
                "Upper Bound     : %0.5f\n"+
                "Lower Bound     : %0.5f\n"
            )%(pair, n_levels, balance, actual_total, upper, lower)
        )
    print(
        "Intended Total: %0.5f"%sum(balances),
        "Actual Total  : %0.5f"%sum(all_actual_totals)
    )

if __name__ == "__main__":
    main()
