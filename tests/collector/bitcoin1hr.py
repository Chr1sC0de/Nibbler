from nibbler.collectors import BinanceBTC

if __name__ == "__main__":
    from pathlib import Path
    directory = Path(__file__).parent/"../../resources/csv"
    assert directory.exists()
    filename = 'BitcoinBinance1hr.csv'
    filepath = directory/filename
    collector = BinanceBTC('1h')
    collector.run(filepath, multiplier=None)