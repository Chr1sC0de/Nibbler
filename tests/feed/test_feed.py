import pathlib as pt
from nibbler.optim.assets import Feed


if __name__ == "__main__":

    cwd = pt.Path(__file__).parent

    csv_files = cwd/"../../resources/csv"
    
    assert csv_files.exists()

    csv_file =csv_files/"BitcoinBinance1hr.csv"

    feed = Feed(csv_file)

    for i, data in enumerate(feed):

        print(data.shape)
        
        if i>20:
            break

