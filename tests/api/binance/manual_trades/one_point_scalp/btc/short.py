import numpy as np
import myconfig
from nibbler.api.agents.binance import TradingAgentSpecialEntries

if __name__ == "__main__":

    agent = TradingAgentSpecialEntries(
        api_key=myconfig.APIKEY,
        secret_key=myconfig.SECRETKEY,
        symbol=myconfig.symbol
    )

    target_price = myconfig.entry_price_short - myconfig.target_diff
    stop         = myconfig.entry_price_short + myconfig.stop_diff

    agent.sell_stop_limit_order(
        price     = myconfig.entry_price_short,
        stopPrice = myconfig.entry_price_short,
        quantity  = myconfig.quantity
    )

    agent.buy_stop_reduce_market_order(
        stopPrice = stop,
        quantity  = myconfig.quantity
    )

    agent.post_buy_order(
        price    = target_price,
        quantity = myconfig.quantity
    )
