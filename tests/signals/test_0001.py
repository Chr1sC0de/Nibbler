
from nibbler import plot
from nibbler.trading.signals.buy.candlesticks import Doji
import pathlib as pt
import pandas as pd
if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    resources_folder = cwd/"../../resources"

    corn_file = resources_folder/"BitcoinBinance1hr.csv"

    signal = Doji()

    df = pd.read_csv(corn_file)[-1000:]

    signallled = signal(df)

    p = signal.plot_features(df)
    # p = signal.plot_signal(df, fig=p)
    plot.show(p)