from . import utils
from ..trading.utils import time_frames

def candlesticks(
        df, lims='all', fig=None, w='4h', skip=0, **kwargs

    ):
    if lims is not 'all':
        df = df[lims[0]:lims[1]]

    df = utils.lower_column_headers(df)
    df = df.iloc[skip:]
    inc = df.close > df.open
    dec = df.open > df.close
    w = time_frames[w]

    p =  utils.initialize_figure(fig, **kwargs)

    scale_width = 0.15

    p.grid.grid_line_alpha=0.3
    p.segment(df.datetime, df.high, df.datetime, df.low, color="black")
    p.vbar(
        df.datetime[inc], w*scale_width, df.open[inc], df.close[inc],
        fill_color="#D5E1DD", line_color="black")
    p.vbar(
        df.datetime[dec], w*scale_width, df.open[dec], df.close[dec],
        fill_color="#F2583E", line_color="black")
    return p

