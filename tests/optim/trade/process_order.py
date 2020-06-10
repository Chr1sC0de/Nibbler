from nibbler.optim import market, trade, exchange
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

    binance = exchange.Exchange("binance")

    binance.addMarket(market)

    iter(market)
    
    for i in range(300):
        next(market)
    
    if False:

        plt.plot(
            market.feeds["4h"][0],
            market.feeds["4h"][2]
        )

        plt.plot(
            market.feeds["1h"][0],
            market.feeds["1h"][2]
        )

        plt.show()

    order = trade.LimitBuy(trader, market, 0.1, 4261, leverage=100)
    counter = i
    rebought = False
    printString = "%0.3f, %0.3f, %0.3f, %0.3f, %0.3f"
    while True:
        counter += 1

        try:
            next(market)
            positionExists = (trader in market.positions.keys())
            if positionExists:
                position = market.positions[trader]
                if not rebought:
                    if counter > 500:
                        trade.LimitSell(trader, market, 0.2, 4540) 
                        position = market.positions[trader]
                        rebought = True
                print(
                    printString%(
                        position.entryPrice, market.getLatestClosePrice(),
                        position.quantity, position.unrealizedPNL(), trader.balance
                    )
                )
            else:
                print(
                    printString%(
                        0, market.getLatestClosePrice(),
                        0, 0, trader.balance 
                    )
                )
            if counter > 1000:
                break
            if trader.balance < 0:
                break
        except:
            break

    trade.MarketBuy(trader, market, 0.1 )

    trader.orders[market].__repr__()

    next(market)

    print(
        printString%(
            0, market.getLatestClosePrice(),
            0, 0, trader.balance 
        )
    )