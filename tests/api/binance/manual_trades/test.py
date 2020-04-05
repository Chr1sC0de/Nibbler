import numpy as np
import config
from nibbler.api.agents.binance import TradingAgentSpecialEntries

if __name__ == "__main__":
    agent = TradingAgentSpecialEntries(
        api_key=config.APIKEY,
        secret_key=config.SECRETKEY
    )

    print("bids")
    print(agent.get_bids())
    print("asks")
    print(agent.get_asks())

    # agent.post_buy_order(price=7600, quantity=0.001)

    atr=100
    mean_price = 5381
    atr_stop_factor = 2.5
    max_risked_quantity = 10
    quantity = max_risked_quantity/(atr_stop_factor*atr)
    stopPrice = mean_price-atr_stop_factor*atr
    stopPrice = np.round(stopPrice,decimals=2)
    priceDeviation = atr/2

    if True:
        orders = agent.risk_based_distributed_buy_entry(
            meanPrice=mean_price,
            stopPrice=stopPrice, quantity=quantity,
            priceDeviation=priceDeviation,
            n_entries=10,
            )

        agent.protect_buy_orders(
            stopPrice=stopPrice,
            orderList=orders)
    else:
        agent.sell_scale_out_buy(
            quantity=0.091,
            meanPrice=7929.16, priceDeviation=priceDeviation,
            n_entries=5
        )
    pass