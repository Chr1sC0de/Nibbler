import nibbler.feeds as nf
import nibbler.markets as nm
import nibbler.exchanges as ne

from nibbler import plt
from make_markets import btcmarket, ontmarket


binance = ne.Exchange("Binance")
binance.addmarkets(btcmarket, ontmarket)


if __name__ == "__main__":

    for i, _ in enumerate(binance):
        if i > 10000:
            f, (ax_1, ax_2) = plt.subplots(2, 1, sharex=True)
            btcmarket.plot_masterohlcv(ax=ax_1)
            ontmarket.plot_masterohlcv(ax=ax_2)
            plt.show()
            plt.close()
