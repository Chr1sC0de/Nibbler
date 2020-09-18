from nibbler import trading as td
import myconfig as mc
from nibbler import api
from pathlib import Path 
from nibbler.trading.stops import atr_stopper
import numpy as np

if __name__ == "__main__":
    # setup the collector

    directory = Path(__file__).parent
    resource_folder = directory/"../../../../resources"
    assert resource_folder.exists()
    filename = 'BitcoinBinance4hr.csv'
    filepath = resource_folder/filename
    collector = td.collectors.BinanceBTC('4h')
    collector.run(filepath)

    # setup the bull, bear and stopper
    signal_paths = Path(__file__).parent/'jljkolj'

    if signal_paths.exists():
        data = np.load(signal_paths)
        bull_signal = data["bull_signal"]
        bear_signal = data["bear_signal"]
    else:
        raise Exception

    # setup the stop calculator
    stop_calculator = atr_stopper

    # setup the trading boi

    agent = api.agents.binance.NibblerAllInAgent(
        collector,
        bull_signal,
        bear_signal,
        stop_calculator=stop_calculator
    )