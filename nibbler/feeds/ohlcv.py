import numpy as np
from bokeh.plotting import figure, output_file, show
from .feed import Feed
from .. import utils


_allnames = ["open", "high", "low", "close"]


class OHLCV(Feed):


    def __init__(self):
        self._tempdata       = None
        self._segments       = None
        self._increment_bars = None
        self._decrement_bars = None

        super(OHLCV, self).__init__()

    def _set_data(self):
        self._data = self._tempdata

    def _object_data(self):
        outputString = "OHLCV: %0.3f/%0.3f/%0.3f/%0.3f/%0.3f"
        return outputString%(
            self.current_open, self.current_high,
            self.current_low, self.current_close,
            self.current_volume
        )

    @property
    def open(self):
        return self._live[1]
    @property
    def high(self):
        return self._live[2]
    @property
    def low(self):
        return self._live[3]
    @property
    def close(self):
        return self._live[4]
    @property
    def volume(self):
        return self._live[5]

    @property
    def current_open(self):
        return self.open[-1]
    @property
    def current_high(self):
        return self.high[-1]
    @property
    def current_low(self):
        return self.low[-1]
    @property
    def current_close(self):
        return self.close[-1]
    @property
    def current_volume(self):
        return self.volume[-1]

    def plot_candlesticks(
        self,
        p               = None,
        plot_width      = 1000,
        title           = None,
        orientation     = np.pi/5,
        grid_line_alpha = 0.3,
        segment_color   = "black",
        increment_color = "green",
        decrement_color = "red",
        bar_width       = 0.6,
        n_bars          = "max",
        tools           = "pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,reset,save"
    ):

        if p is None:
            p = figure(
                x_axis_type = "datetime",
                tools       = tools,
                plot_width  = plot_width,
                title       = title
            )
            p.xaxis.major_label_orientation = orientation
            p.grid.grid_line_alpha          = grid_line_alpha

        datetime       = utils.timeframeconversion.timestamp_to_datetime(self.datetime)
        datetime_width = np.gradient(self.datetime)*bar_width

        if n_bars == "max":
            d_open  = self.open
            d_high  = self.high
            d_low   = self.low
            d_close = self.close
        else:
            n_bars         = np.clip(n_bars, 2, len(self.open))
            d_open         = self.open[-n_bars:]
            d_high         = self.high[-n_bars:]
            d_low          = self.low[-n_bars:]
            d_close        = self.close[-n_bars:]
            datetime       = datetime[-n_bars:]
            datetime_width = datetime_width[-n_bars:]

        incr = d_close > d_open
        decr = d_close < d_open

        self._segments       = p.segment(
            datetime, d_high, datetime, d_low, color=segment_color)

        self._increment_bars = p.vbar(
            datetime[incr], datetime_width[incr], d_open[incr], d_close[incr],
            fill_color = increment_color,
            line_color = "black"
        )
        self._decrement_bars = p.vbar(
            datetime[decr], datetime_width[decr], d_open[decr], d_close[decr],
            fill_color = decrement_color,
            line_color = "black"
        )
        return p

    def plot_volume(
        self,
        p               = None,
        plot_width      = 1000,
        title           = None,
        orientation     = np.pi/5,
        grid_line_alpha = 0.3,
        segment_color   = "black",
        increment_color = "green",
        decrement_color = "red",
        bar_width       = 0.6,
        n_bars          = "max",
        tools           = "pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,reset,save"
    ):
        if p is None:
            p = figure(
                x_axis_type = "datetime",
                tools       = tools,
                plot_width  = plot_width,
                title       = title
            )
            p.xaxis.major_label_orientation = orientation
            p.grid.grid_line_alpha          = grid_line_alpha

    def plot(self, p):
        pass
