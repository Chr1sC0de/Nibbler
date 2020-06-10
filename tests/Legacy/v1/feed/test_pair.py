import pathlib as pt
from nibbler.optim.assets import Feed
from nibbler.optim.assets import Market

if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../resources/csv"
    
    assert csv_files.exists()

    csv_file_1hr =csv_files/"BitcoinBinance1hr.csv"
    csv_file_4hr =csv_files/"BitcoinBinance4hr.csv"

    feed_1hr = Feed(csv_file_1hr)
    feed_4hr = Feed(csv_file_4hr)

    pair = Market("btc/usd")

    pair.add_feed(feed_4hr)
    pair.add_feed(feed_1hr)

    for minutes, feed in pair.feed_list:
        print(len(feed))
        print(feed.wait)
    
    print(len(pair))

    counter = 0

    for data in pair:
        counter += 1
        if counter % 100 == 0:
            break

        for key, val in data.items():
            print(key, val.shape)