import pathlib as pt
import nibbler.feeds as nf
import nibbler.markets as nm
from nibbler import plt


class TestMarket(nm.Market):
    def processorder(self):
        pass


if __name__ == "__main__":

    cwd         = pt.Path(__file__).parent
    data_folder = cwd/"../../resources/data"

    assert data_folder.exists()

    filename_1    = "ONT_USD_1h.csv"
    filename_2    = "ONT_USD_4h.csv"

    filepath_1    = data_folder/filename_1
    filepath_2    = data_folder/filename_2

    feed_1 = nf.csv.OHLCV(filepath_1)
    feed_2 = nf.csv.OHLCV(filepath_2)

    btcmarket = TestMarket("ONT", "USDT")

    btcmarket.addfeeds(feed_2, feed_1)

    print(btcmarket.feeds)
    print(btcmarket.feedsohlcv)
    print(btcmarket.masterfeed)