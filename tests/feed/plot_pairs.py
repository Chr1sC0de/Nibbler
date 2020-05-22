import matplotlib.pyplot as plt
import pathlib as pt
from nibbler.optim.assets import Feed
from nibbler.optim.assets import Pair

if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../resources/csv"
    
    assert csv_files.exists()

    csv_file_1hr =csv_files/"BitcoinBinance1hr.csv"
    csv_file_4hr =csv_files/"BitcoinBinance4hr.csv"

    feed_1hr = Feed(csv_file_1hr)
    feed_4hr = Feed(csv_file_4hr)

    pair =Pair("btc/usd")

    pair.add_feed(feed_4hr)
    pair.add_feed(feed_1hr)

    for data in pair:

        for key in data.keys():
            time_data = data[key]
            plt.plot(time_data[0], time_data[3])
        
        plt.show()