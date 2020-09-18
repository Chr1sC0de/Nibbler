from add_trader import (
    trader, binance, btcmarket, ontmarket)
import nibbler.orders as no
import pathlib as pt
from nibbler import plt


if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    buy_ordered         = False
    sell_ordered        = False
    market_buy_ordered  = False
    market_sell_ordered = False

    stop_limit_buy_ordered   = False
    stop_limit_sell_ordered  = False
    stop_market_buy_ordered  = False
    stop_market_sell_ordered = False

    savefolder = cwd/"make_spot_order_images"

    if not savefolder.exists():
        savefolder.mkdir()

    image_counter = 0

    for i, _ in enumerate(binance):

        usdtwallet = trader.spotwallets["USDT"]
        btcwallet  = trader.spotwallets["BTC"]


        if i > 114:

            f = plt.figure(figsize=(21, 11))

            btcmarket.plot_masterohlcv()

            if not buy_ordered:
                no.spot.limit.Buy(
                    btcmarket,
                    trader,
                    0.1,
                    3800
                )
                buy_ordered = True

            try:
                if not sell_ordered:
                    no.spot.limit.Sell(
                        btcmarket,
                        trader,
                        0.1,
                        4000
                    )
                    sell_ordered = True
            except:
                pass

            if i > 120:
                if not market_buy_ordered:
                    no.spot.market.Buy(
                        btcmarket,
                        trader,
                        0.1,
                    )
                    market_buy_ordered = True

            if i > 125:
                if not market_sell_ordered:
                    no.spot.market.Sell(
                        btcmarket,
                        trader,
                        btcwallet.balance,
                    )
                    market_sell_ordered = True

            if i > 130:
                if not stop_limit_buy_ordered:
                    no.spot.stop.limit.Buy(
                        btcmarket,
                        trader,
                        0.1,
                        3700,
                        3800
                    )
                    stop_limit_buy_ordered = True

            for market in binance.spotmarkets.values():
                market.plot_orders()
                market.plot_stops()

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