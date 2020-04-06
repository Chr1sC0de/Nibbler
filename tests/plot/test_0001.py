from nibbler import trading as td
from nibbler import plot
import pathlib as pt
import pandas as pd
if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    resources_folder = cwd/"../../resources"

    corn_file = resources_folder/"BitcoinBinance1hr.csv"

    p = plot.csv.candlesticks(corn_file, skip=20000)

    plot.show(p)

    df = pd.read_csv(corn_file)
    plot.show(plot.candlesticks(df))