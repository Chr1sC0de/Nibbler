from make_exchange import binance
from nibbler import traders

trader = traders.MinMax()

# ---------------------- register a wallet to the trader --------------------- #
trader.addwallets(traders.wallets.Spot("USDT", 1000))
# -------------------- register the trader to an exchange -------------------- #
trader.register_to_exchange(binance)

if __name__ == "__main__":
    for i, _ in enumerate(binance):
        if i > 1000:
            pass