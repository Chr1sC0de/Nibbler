secondsToTimeframe = {
    1000*60:"m",
    1000*60*60:"h",
    1000*60*60*24:"d",
    1000*60*60*24*7:"w"
}
timeframeToSeconds = {
    "m": 1000*60,
    "h": 1000*60*60,
    "d": 1000*60*60*24,
    "w": 1000*60*60*24*7
}
from . import market
from . import exchange
from . import trade

