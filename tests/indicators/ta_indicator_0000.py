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
    indicator = indicators.Indicator(trend.ema_indicator)
    indicator_values = indicator(df)
    p = plot.candlesticks(df)

    sg_filter = indicators.trend.SavitzkyGolayOpen()
    sg_filter.plot(df, fig=p)
    plot.show(indicator.plot(df, fig=p))

    sg_filter = indicators.trend.SavitzkyGolayLow.random_initialization(20,100,3,7)

    sg_filter.plot(df, fig=p)
    plot.show(p)