from . import candlesticks as df_candlesticks
import pandas as pd
import pathlib as pt

def candlesticks(path, **kwargs):
    csv_path = pt.Path(path)
    data = pd.read_csv(csv_path.as_posix()) 

    return df_candlesticks(data, **kwargs)

