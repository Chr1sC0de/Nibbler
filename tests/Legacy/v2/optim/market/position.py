from nibbler.optim.market import Market, CSVFeed
from nibbler.optim.exchange import Exchange
from nibbler.optim.trader import Trader, Order
import pathlib as pt
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    cwd = pt.Path(__file__).parent

    resourceFolder = cwd/"../../../resources/csv"

    assert resourceFolder.exists()

    dataPath4hr = resourceFolder/"BitcoinBinance4hr.csv"
    dataPath1hr = resourceFolder/"BitcoinBinance1hr.csv"

    assert dataPath4hr.exists()
    assert dataPath1hr.exists()

    feed4hr = CSVFeed(dataPath4hr)
    feed1hr = CSVFeed(dataPath1hr)

    market = Market("BTC")

    market.addFeed(feed4hr)
    market.addFeed(feed1hr)

    trader = Trader()

    exchange = Exchange(0.001, 0.001)

    exchange.addMarket(market)
    exchange.addTrader(trader)

    exchange.initialize()

    print(exchange.availableMarkets())

    order = Order(trader, market, 1, 4000)

    print(market.orders)

    order.close()

    print(market.orders)

    for i in range(100):
        exchange.step()
        print(exchange.markets["BTC"].feeds["1h"].shape)
        print(exchange.markets["BTC"].feeds["4h"].shape)
        plt.plot(
            exchange.markets["BTC"].feeds["1h"][0],
            exchange.markets["BTC"].feeds["1h"][1]
        )
        plt.plot(
            exchange.markets["BTC"].feeds["4h"][0],
            exchange.markets["BTC"].feeds["4h"][1]
        )
        plt.show()