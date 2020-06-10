from . import utils

time_frames = {
    '1m': 60*1000,
    '5m': 60*1000,
    '15m': 60*1000,
    '1h': 60*60*1000,
    '2h': 2*60*60*1000,
    '4h': 4*60*60*1000,
    '12h': 12*60*60*1000,
    'd': 24*60*60*1000,
    'w': 7*24*60*60*1000,
    'M': 30*24*60*60*1000,
}

def candlesticks(dohlcv, lims="all", fig=None, width="4h", **kwargs ):

    if lims is not "all":
        # lims is either a string or some ellipses
        dohlcv = dohlcv[lims]
    
    dfDatetime = dohlcv[0]
    dfopen = dohlcv[1]
    dfhigh = dohlcv[2]
    dflow = dohlcv[3]
    dfclose = dohlcv[4]

    inc = dfclose > dfopen
    dec = dfclose < dfopen 

    scale_width = 0.15
    width = time_frames[width]

    p = utils.initialize_figure(fig, **kwargs)
    p.grid.grid_line_alpha = 0.3
    p.line(dfDatetime, dfclose)
    # p.segment(
    #     dfDatetime, dfhigh, dfDatetime, dflow, color="black"
    # )
    # p.vbar(
    #     dfDatetime[inc], width*scale_width, dfopen[inc], dfclose[inc],
    #     fill_color="#D5E1DD", line_color="black"
    # )
    # p.vbar(
    #     dfDatetime[dec], width*scale_width, dfopen[dec], dfclose[dec],
    #     fill_color="#F2583E", line_color="black"
    # )
    return p


