import matplotlib.pyplot as plt

def candlesticks(dohlcv, ax=None, volPercent=0.2, figsize=(21,11), **kwargs):

    if ax == None:
        fig = plt.figure(figsize=figsize)
        fig.tight_layout()
        ax = fig.add_subplot(111)
    
    d_datetime = dohlcv[0]
    d_open = dohlcv[1]
    d_high = dohlcv[2]
    d_low = dohlcv[3]
    d_close = dohlcv[4]
    
    ax.plot(d_datetime, d_open, "g")
    ax.plot(d_datetime, d_close, "r")
    ax.plot(d_datetime, d_high, "k")
    ax.plot(d_datetime, d_low, "k")

    return ax

def volume(dohlcv, ax):

    ylims = ax.get_ylim()

    d_datetime = dohlcv[0]
    d_volume = dohlcv[5]

    volMin = ylims[0]*(1-0.1)
    volMax = volMin + (ylims[1] - volMin)*0.2

    # scale the volume to between 0 and 1
    tauVolume = d_volume - d_volume.min()
    tauVolume = tauVolume/tauVolume.max()

    # rescale the volume
    rescaledVolume = (volMax-volMin) * (tauVolume) + volMin

    ax.plot(d_datetime, rescaledVolume)

    return ax


