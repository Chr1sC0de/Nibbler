import numpy as np
import myconfig
from nibbler.api.agents.binance import TradingAgentSpecialEntries

if __name__ == "__main__":

    agent = TradingAgentSpecialEntries(
        api_key=myconfig.APIKEY,
        secret_key=myconfig.SECRETKEY,
        symbol="ADAUSDT"
    )


    target_diff = 0.00040
    stop_diff   = 0.00080

    entry_price  = 0.13941
    target_price = entry_price + target_diff
    stop         = entry_price - stop_diff

    quantity = 1250

    # agent.buy_stop_market_order(
    #     stopPrice = entry_price,
    #     # price     = entry_price-0.00001,
    #     quantity  = quantity
    # )

    agent.buy_stop_market_order(
        stopPrice = entry_price,
        price     = entry_price,
        quantity  = quantity
    )

    agent.sell_stop_reduce_buy_market(
        stopPrice=stop, quantity=quantity
    )

    agent.post_sell_order(
        price     = target_price,
        quantity  = quantity
    )
