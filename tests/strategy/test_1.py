import nibbler as nd
from nibbler.trading import signals
from nibbler.trading import strategy
from nibbler import plot
import pandas as pd
import pathlib as pt

cwd = pt.Path(__file__).parent
resource_folder = cwd/"../../resources"

data_file = resource_folder/"BitcoinBinance1hr.csv"
dataframe = pd.read_csv(data_file)

if __name__ == "__main__":

    buy_signal = signals.buy.SavitzkyGolayMin()
    sell_signal = signals.sell.SavitzkyGolayMax()

    strategy = strategy.MarketLong(
        buy_signal, sell_signal,
        leverage = 1,
        use_leverage = True
    )

    strategy.walk_dataset(dataframe.iloc[0:5000])
    plot.show(
        strategy.plot_trade_and_equity()
    )
    print(strategy.trade_log)
    strategy.save("strat")
