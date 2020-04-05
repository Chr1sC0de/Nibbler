from nibbler import trading as td
if __name__ == "__main__":
    from pathlib import Path
    directory = Path(__file__).parent
    filename = 'CORNance.csv'
    filepath = directory/filename
    collector = td.collectors.BinanceBTC('1h')
    collector.run(filepath, multiplier=4)