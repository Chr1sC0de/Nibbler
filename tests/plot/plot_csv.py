from nibbler import trading as td
from nibbler import plot
import pathlib as pt

if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    collector_folder = cwd/"../collectors"

    corn_file = collector_folder/"CORNance.csv"

    p = plot.csv.candlesticks(corn_file, skip=20000)

    plot.show(p)



