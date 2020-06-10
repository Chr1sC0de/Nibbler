from bokeh import models
from ..optim import market, trade


def position(pos, fig, *args, **kwargs):
    assert isinstance(pos, market.Position)

    if pos.positionType == "longPosition":  
        span = models.Span(
            location=pos.entryPrice, line_color="green", line_width=3) 
    if pos.positionType == "shortPosition":
        span = models.Span(
            location=pos.entryPrice, line_color="red", line_width=3) 
    entryPice = models.Label(
        y=pos.entryPrice*1.001,
        x=pos.market.feeds[pos.market.smallestTimeframe][0][-400],
        text="entryPrice=%0.3f, quantity=%0.3f, balance=%0.3f"%(
            pos.entryPrice, pos.quantity, pos.trader.balance),
        text_font_size="20pt"
    )
    fig.add_layout(span)
    fig.add_layout(entryPice)
    return fig

def order(order, fig, *args, **kwargs):
    assert isinstance(order, trade.Order)

    if order.orderType == "limitBuy":  
        span = models.Span(
            location=order.entryPrice, line_color="green", line_width=3, line_dash="dashed") 
    if order.orderType == "limitSell":
        span = models.Span(
            location=order.entryPrice, line_color="red", line_width=3,line_dash="dashed")
    if order.orderType == "stopMarketBuy":
        span = models.Span(
            location=order.stop, line_color="green", line_width=3,line_dash="dashed") 
    if order.orderType == "stopMarketSell":
        span = models.Span(
            location=order.stop, line_color="red", line_width=3,line_dash="dashed")  
    if "market" in order.orderType.lower():
        if "stop" in order.orderType:
            text = "stopMarket=%0.3f, quantity=%0.3f"%(order.stop, order.quantity)
            entry = order.stop
        else:
            return fig
    else:
        text = "entryPrice=%0.3f, quantity=%0.3f"%(order.entryPrice, order.quantity)
        entry = order.entryPrice
    entryPice = models.Label(
        y=entry*1.001,
        x=order.market.feeds[order.market.smallestTimeframe][0][-400],
        text=text,
        text_font_size="20pt"
    )
    fig.add_layout(span)
    fig.add_layout(entryPice)
    return fig
