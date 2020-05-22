from .time_frame_multiplier import (
    time_frame_multiplier
)

def lower_column_headers(data_frame):
    data_frame.columns = data_frame.columns.str.lower()
    return data_frame

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