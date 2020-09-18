import pathlib as pt
import nibbler.feeds as nf


if __name__ == "__main__":
    cwd         = pt.Path(__file__).parent
    data_folder = cwd/"../../resources/data"
    assert data_folder.exists()
    filename    = "ONT_USD_4h.csv"
    filepath    = data_folder/filename

    feed = nf.csv.OHLCV(filepath)

    for i, _ in enumerate(feed):
        if i>10:
            break

    print(feed.datetime[-4:])
    print(feed.open[-4:])
    print(feed.high[-4:])
    print(feed.low[-4:])
    print(feed.close[-4:])
    print(feed.volume[-4:])
    print(feed.currentdatetime)
    print(feed.currentopen)
    print(feed.currenthigh)
    print(feed.currentlow)
    print(feed.currentclose)
    print(feed.currentvolume)
    print(feed.startdatetime)