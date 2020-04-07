
from nibbler import plot
from nibbler.trading.signals.buy import SavitzkyGolayMin
from nibbler.trading.signals.sell import SavitzkyGolayMax
import pathlib as pt
import pandas as pd
if __name__ == "__main__":
    cwd = pt.Path(__file__).parent

    resources_folder = cwd/"../../resources"

    corn_file = resources_folder/"BitcoinBinance1hr.csv"

    signal = SavitzkyGolayMin()
    signal_max = SavitzkyGolayMax()

    df = pd.read_csv(corn_file)[-100:]

    signallled = signal(df)

    p = signal.plot_features(df)
    p = signal.plot_signal(df, fig=p)
    p = signal_max.plot_features(df, fig=p)
    plot.show(p)