import pathlib as pt
from nibbler.optim.feed import Feed
from time import time


if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../resources/csv"
    
    assert csv_files.exists()

    csv_file =csv_files/"BitcoinBinance1hr.csv"

    feed = Feed(csv_file)

    N = 10000000

    start = time()

    for data in feed:
        pass

    end = time()

    print(end-start)

    # time the fee without the generator

    start = time()

    for i in range(len(feed)):
        i += 500
        feed.data[:, 0:i]

    end = time()

    print(end-start)

    # we observe that it is faster to use the data feed directly rather than the generator
    # however it does not make a lot of difference as to what we use 