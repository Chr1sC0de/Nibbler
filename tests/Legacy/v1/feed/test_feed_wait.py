import pathlib as pt
from nibbler.optim.assets import Feed


if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../resources/csv"
    
    assert csv_files.exists()

    csv_file_1hr = csv_files/"BitcoinBinance1hr.csv"
    csv_file_4hr = csv_files/"BitcoinBinance4hr.csv"

    feed_1hr = Feed(csv_file_1hr, wait=0)
    feed_4hr = Feed(csv_file_4hr, wait=4)

    print(len(feed_1hr))
    print(len(feed_4hr))

    for i, (data_1hr, data_4hr) in enumerate(zip(feed_1hr, feed_4hr)):

        print(data_1hr[0, -1] < data_4hr[0, -1])

        if i>20:
            break

