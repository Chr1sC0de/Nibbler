import click
import myconfig as mc
import numpy as np
from binance.client import Client

precisions = {
    "ADAUSDT"  : {"price": 5, "quantity": 0 },
    "ALGOUSDT" : {"price": 4, "quantity": 2 },
    "BANDUSDT" : {"price": 4, "quantity": 1 },
    "BCHUSDT"  : {"price": 2, "quantity": 3 },
    "BLZUSDT"  : {"price": 5, "quantity": 1 },
    "DOTUSDT"  : {"price": 3, "quantity": 1 },
    "LINKUSDT" : {"price": 3, "quantity": 2 },
    "MATICUSDT": {"price": 5, "quantity": 1 },
    "OMGUSDT"  : {"price": 4, "quantity": 1 },
    "SXPUSDT"  : {"price": 4, "quantity": 1 },
    "WAVESUSDT": {"price": 4, "quantity": 1 },
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