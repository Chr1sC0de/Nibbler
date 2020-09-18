import pathlib as pt
import nibbler.feeds as nf
from nibbler import plt


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

    feed_2.setmaster(feed_1)

    if False:
        for i, _ in enumerate(feed_1):
            if i > 100:
                f, ax = plt.subplots(2, 1, sharex=True)
                feed_1.plot(ax=ax[0])
                feed_2.plot(ax=ax[1])
                plt.show()
                plt.close()

    print(feed_1._children)
    print(feed_2._master)
    feed_2.delmaster()
    print(feed_1._children)
    print(feed_2._master)