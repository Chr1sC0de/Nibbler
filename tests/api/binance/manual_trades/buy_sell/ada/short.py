import numpy as np
import myconfig
from nibbler.api.agents.binance import TradingAgentSpecialEntries

if __name__ == "__main__":

    agent = TradingAgentSpecialEntries(
        api_key=myconfig.APIKEY,
        secret_key=myconfig.SECRETKEY,
        symbol="ADAUSDT"
    )

    target_price = myconfig.entry_price - myconfig.target_diff
    stop         = myconfig.entry_price + myconfig.stop_diff

        price     = myconfig.entry_price,
        quantity  = myconfig.quantity
    )

    agent.buy_stop_market_order(
        stopPrice = stop,
        quantity  = myconfig.quantity
    )

    agent.post_buy_order(
        price     = target_price,
        quantity  = myconfig.quantity
    )
