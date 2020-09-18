import datetime as _dt
import numpy as _np


def convertTimestampToDatetime(datetime):

    if not isinstance(datetime[0], _dt.datetime):
        datetime = [
            _dt.datetime.fromtimestamp(int(date)/1000)
            for date in datetime
        ]

    return _np.array(datetime)


def hideDatetimeAxis(ax):
    ax.set_xticklabels([])
    ax.set_xlabel(None)
    ax.tick_params("x", length=0)
    ax.spines["bottom"].set_color("none")
    return ax


def styleAxis(ax, rotation=50):
    ax.minorticks_on()
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    ax.tick_params(axis='x', labelrotation=rotation)
    ax.grid(True, linestyle="--", alpha=0.5)

    return ax