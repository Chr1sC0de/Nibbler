# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 20:37:47 2019

@author: chris
"""
import pandas as pd
import numpy as np
from typing import List
from tqdm import tqdm

def time_frame_multiplier(
    data_frame, time_factor,
    columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'],
    include_datetime=True
):
    n_entries = len(data_frame)//time_factor
    df = pd.DataFrame(
        columns=columns,
        index=np.arange(n_entries)
    )
    for i in np.arange(n_entries):
        # if all([len(tmp)%time_factor == 0,len(tmp) >0]) :
        tmp = \
            data_frame.loc[i*time_factor:((i+1)*time_factor-1)][columns].values
        # now it is time to populate the dataframe
        df.loc[i][columns] = \
            [
                tmp[0, 0],
                tmp[0, 1],
                np.max(tmp[:, 1]),
                np.min(tmp[:, 2]),
                tmp[-1, 4],
                np.sum(tmp[:, -1])
            ]
    return df.dropna()
