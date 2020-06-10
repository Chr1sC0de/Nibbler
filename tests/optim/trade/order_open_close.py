from nibbler.optim import market, trade
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

    market = market.Market("USD", "BTC")

    market.addFeed(feed4hr)
    market.addFeed(feed1hr)

    trader = trade.Trader()

    order = trade.Order(trader, market, 1, 700)

    print(market.orders)

    order.close()

    print(market.orders)
    
    
