from nibbler.optim import market
import pathlib as pt
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    cwd = pt.Path(__file__).parent

    resourceFolder = cwd/"../../../resources/csv"

    assert resourceFolder.exists()

    dataPath = resourceFolder/"BitcoinBinance4hr.csv"

    assert dataPath.exists()

    feed = market.CSVFeed(dataPath)

    for data in feed:
        if data is not None:
            plt.plot(data[0], data[1])
            plt.show()