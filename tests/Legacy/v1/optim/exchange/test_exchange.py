from nibbler import optim
import pathlib as pt
from collections import OrderedDict

cwd = pt.Path(__file__).parent
csv_files = cwd/"../../../resources/csv"
assert csv_files.exists()
csv_file =csv_files/"BitcoinBinance1hr.csv"


if __name__ == "__main__":

    feed = optim.feed.Feed(csv_file)
    user = optim.user.User()

    feed_dict = OrderedDict(
        bitcoin1hr=feed
    )

    exchange = optim.exchange.Exchange(user, feed_dict)
