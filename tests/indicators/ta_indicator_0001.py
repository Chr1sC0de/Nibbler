from nibbler.trading import indicators
from nibbler import plot
import pandas as pd

if __name__ == "__main__":
    from ta import momentum, trend
    import pathlib as pt
    cwd = pt.Path(__file__).parent
    resources_folder = cwd.parent/"../resources"
    csv_file = resources_folder/"BitcoinBinance1hr.csv"

    df = pd.read_csv(csv_file)
    indicator = indicators.trend.MinFinderLow()
    indicator = indicators.trend.MinFinderLow.random_initialization()
    indicator_values = indicator(df)
    p = plot.candlesticks(df)
    indicator.plot(df, fig=p)
    plot.show(p)