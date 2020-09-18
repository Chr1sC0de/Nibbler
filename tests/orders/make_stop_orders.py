from add_trader import (
    trader, binance, btcmarket, ontmarket)
import nibbler.orders as no
import pathlib as pt
from nibbler import plt


if __name__ == "__main__":

    cwd = pt.Path(__file__).parent
    limit_buy_ordered        = False
    stop_limit_buy_ordered   = False
    stop_limit_sell_ordered  = False
    stop_market_buy_ordered  = False
    stop_market_sell_ordered = False

    savefolder = cwd/"make_spot_stop_order_images"

    if not savefolder.exists():
        savefolder.mkdir()

    image_counter = 0

    for i, _ in enumerate(binance):

        usdtwallet = trader.spotwallets["USDT"]
        btcwallet  = trader.spotwallets["BTC"]

        if i > 114:

            f = plt.figure(figsize=(21, 11))
            ax = plt.gca()

            btcmarket.plot_masterohlcv()

            if not limit_buy_ordered:
                no.spot.limit.Buy(
                    btcmarket,
                    trader,
                    0.1,
                    3800
                )
                limit_buy_ordered = True

            if btcwallet.balance > 0:
                if not stop_limit_sell_ordered:
                    no.spot.stop.limit.Sell(
                        btcmarket,
                        trader,
                        btcwallet.balance,
                        3450,
                        3600
                    )
                    stop_limit_sell_ordered = True

            for market in binance.spotmarkets.values():
                market.plot_orders(ax=ax)
                market.plot_stops(ax=ax)

            f.savefig(
                savefolder/("%05d"%image_counter),
                dpi     = 100,
            )

            plt.close()

            image_counter += 1

            if i > 200:
                break

            print(usdtwallet)
            print(btcwallet)