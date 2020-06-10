from nibbler.optim import market
import pathlib as pt
import matplotlib.pyplot as plt
from time import time


if __name__ == "__main__":
    
    cwd = pt.Path(__file__).parent

    resourceFolder = cwd/"../../../resources/csv"

    assert resourceFolder.exists()

    dataPath4hr = resourceFolder/"BitcoinBinance4hr.csv"
    dataPath1hr = resourceFolder/"BitcoinBinance1hr.csv"

    assert dataPath4hr.exists()
    assert dataPath1hr.exists()

    feed4hr = market.CSVFeed(dataPath4hr)
    feed1hr = market.CSVFeed(dataPath1hr)

    market = market.Market("BTC")

    market.addFeed(feed4hr)
    market.addFeed(feed1hr)

    print(market.availableFeeds())
    print(market.smallestTimeframe)

    print(len(market))

    start = time()
    for data in market:
        if False:
            plt.plot(
                data["1h"][0,:], data["1h"][1,:], "r"
            )
            try:
                plt.plot(
                    data["4h"][0,:], data["4h"][1,:], "g"
                )
            except:
                pass
            plt.show()
    end = time()
    print(end-start)