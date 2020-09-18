import numpy as np
import myconfig
from nibbler.api.agents.binance import TradingAgentSpecialEntries

if __name__ == "__main__":

    agent = TradingAgentSpecialEntries(
        api_key=myconfig.APIKEY,
        secret_key=myconfig.SECRETKEY,
        symbol=myconfig.symbol
    )

    target_price = myconfig.entry_price + myconfig.target_diff
    stop         = myconfig.entry_price - myconfig.stop_diff

    agent.buy_stop_limit_order(
        stopPrice = myconfig.entry_price,
        price     = myconfig.entry_price,
        quantity  = myconfig.quantity
    )

    # agent.sell_stop_reduce_buy_market(
    #     stopPrice = stop,
    #     quantity  = myconfig.quantity
    # )

    # agent.post_sell_order(
    #     price     = target_price,
    #     quantity  = myconfig.quantity
    # )
