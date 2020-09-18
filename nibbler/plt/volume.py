import matplotlib.pyplot as plt
from . import utils


def volumeOnScreen(feed , ax=None, screenFactor=0.15, indexes=None):

    if ax is None:
        f = plt.figure()
        ax = f.add_subplot(111)

    if indexes is None:
        datetime = feed.datetime
        dvolume  = feed.volume
    else:
        datetime = feed.datetime[indexes[0]:indexes[-1]]
        dvolume  = feed.volume[indexes[0]:indexes[-1]]

    datetime = utils.convertTimestampToDatetime(datetime)
    ylims    = ax.get_ylim()

    volMin = ylims[0]*(1-0.1)
    volMax = volMin + (ylims[1] - volMin)*screenFactor
    # scale the dvolume to between 0 and 1
    tauVolume = dvolume - dvolume.min()
    tauVolume = tauVolume/tauVolume.max()
    # rescale the dvolume
    rescaledVolume = (volMax-volMin) * (tauVolume) + volMin

    ax.plot_date(datetime, rescaledVolume, "-", alpha=0.8)

    return ax
