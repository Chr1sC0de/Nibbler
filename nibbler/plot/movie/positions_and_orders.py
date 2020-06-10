import matplotlib.pyplot as plt
from matplotlib import transforms
from ...optim import market, trade


def position(feed, pos, ax):
    assert isinstance(pos, market.Position)

    xlim = (feed[0].min(),feed[0].max())
    entryPrice = (pos.entryPrice, pos.entryPrice)

    string = \
        "Kind      : %s\nEntry     : %0.3f\nQuantity: %0.3f\
            \nBalance : %0.3f\nMargin  : %0.3f\npnl     : %0.3f\nleverage: %0.3f"
            
    if pos.positionType == "longPosition":
        string = string%(
            "long", pos.entryPrice, pos.quantity, pos.trader.balance,
            pos.getMargin(), pos.unrealizedPNL(), pos.leverage
        )
        ax.plot(xlim, entryPrice, "g")
    else:
        string = string%(
            "short", pos.entryPrice, pos.quantity, pos.trader.balance,
            pos.getMargin(), pos.unrealizedPNL(), pos.leverage
        )
        ax.plot(xlim, entryPrice, "r")

    trans = transforms.blended_transform_factory(
		ax.transAxes, ax.transData)

    ax.text(
        1.01, y=entryPrice[0], s=string,
        verticalalignment="center", transform=trans
    ) 
    return ax


def order(feed, order, ax):

    assert isinstance(order, trade.Order)

    string = "Kind: %s, Entry: %0.3f, Quantity: %0.3f"
    kind = None
    orderType = order.orderType.lower()

    xlim = (feed[0].min(),feed[0].max())
    if "limit" in orderType:
        ylim = (order.entryPrice, order.entryPrice)
        kind = "limit"
    if "market" in orderType:
        if "stop" in orderType:
            ylim = (order.stop, order.stop)
            kind = "stopMarket"
        else:
            return ax
    
    string = string%(kind, ylim[0], order.quantity)
    if "buy" in orderType:
        ax.plot(xlim, ylim, "g--")
    else:
        ax.plot(xlim, ylim, "r--")

    trans = transforms.blended_transform_factory(
		ax.transAxes, ax.transData)

    ax.text(
        0.5, ylim[0]*0.9925, s=string, ha="left", transform=trans
    ) 

    return ax
