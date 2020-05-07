from nibbler import trading as td
import myconfig as mc
from nibbler import api
from pathlib import Path 

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


    # setup the trading boi

    agent = api.agents.binance.NibblerAllInAgent(

    )