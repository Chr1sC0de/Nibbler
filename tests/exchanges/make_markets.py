import pathlib as pt
import nibbler.feeds as nf
import nibbler.markets as nm
from nibbler import plt



cwd         = pt.Path(__file__).parent
data_folder = cwd/"../../resources/data"

assert data_folder.exists()

# ---------------------- initialize the ontology market ---------------------- #
ont_filename_1    = "ONT_USD_1h.csv"
ont_filename_2    = "ONT_USD_4h.csv"
ont_filename_3    = "ONT_USD_1d.csv"
ont_filepath_1    = data_folder/ont_filename_1
ont_filepath_2    = data_folder/ont_filename_2
ont_filepath_3    = data_folder/ont_filename_3

ont_feed_1 = nf.csv.OHLCV(ont_filepath_1)
ont_feed_2 = nf.csv.OHLCV(ont_filepath_2)
ont_feed_3 = nf.csv.OHLCV(ont_filepath_1)

ontmarket = nm.Spot("ONT", "USDT")

ontmarket.addfeeds(
    ont_feed_2,
    ont_feed_1,
    ont_feed_3
)
# ---------------------- initialize the bitcoin markets ---------------------- #
btc_filename_1    = "BTC_USDT_1m.csv"
btc_filename_2    = "BTC_USDT_5m.csv"
btc_filename_3    = "BTC_USDT_15m.csv"
btc_filename_4    = "BTC_USDT_1h.csv"
btc_filename_5    = "BTC_USDT_4h.csv"
btc_filename_6    = "BTC_USDT_1d.csv"
btc_filepath_1    = data_folder/btc_filename_1
btc_filepath_2    = data_folder/btc_filename_2
btc_filepath_3    = data_folder/btc_filename_3
btc_filepath_4    = data_folder/btc_filename_4
btc_filepath_5    = data_folder/btc_filename_5
btc_filepath_6    = data_folder/btc_filename_6

btc_feed_1 = nf.csv.OHLCV(btc_filepath_1)
btc_feed_2 = nf.csv.OHLCV(btc_filepath_2)
btc_feed_3 = nf.csv.OHLCV(btc_filepath_3)
btc_feed_4 = nf.csv.OHLCV(btc_filepath_4)
btc_feed_5 = nf.csv.OHLCV(btc_filepath_5)
btc_feed_6 = nf.csv.OHLCV(btc_filepath_6)

btcmarket = nm.Spot("BTC", "USDT")

btcmarket.addfeeds(
    btc_feed_1,
    btc_feed_2,
    btc_feed_3,
    btc_feed_4,
    btc_feed_5,
    btc_feed_6
)

# ---------------------------------------------------------------------------- #
#                       test that the markets are working                      #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":

    f, (ax_1, ax_2) = plt.subplots(2, 1)
    for i, _ in enumerate(zip(btcmarket, ontmarket)):
        if i > 100:
            btcmarket.plot(ax=ax_1)
            ontmarket.plot(ax=ax_2)
            plt.show()
            plt.close()
            break