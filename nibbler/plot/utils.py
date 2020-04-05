import pathlib as pt
import pandas as pd

from bokeh.plotting import figure, output_file, show

TOOLS = "pan,wheel_zoom,ywheel_zoom,xwheel_zoom,box_zoom,reset,save"
DATETIME = 'datetime'


def lower_column_headers(data_frame):
    data_frame.columns = data_frame.columns.str.lower()
    return data_frame


def initialize_figure(p, **kwargs):
    if p is not None:
        return p
    return figure(
        x_axis_type=DATETIME,
        tools=TOOLS, **kwargs
    )
