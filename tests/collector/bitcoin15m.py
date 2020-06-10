from nibbler.collectors import BinanceBTC

if __name__ == "__main__":
    from pathlib import Path
    directory = Path(__file__).parent/"../../resources/csv"
    assert directory.exists()
    filename = 'BitcoinBinance15m.csv'
    filepath = directory/filename
    collector = BinanceBTC('15m')
    collector.run(filepath, multiplier=None)