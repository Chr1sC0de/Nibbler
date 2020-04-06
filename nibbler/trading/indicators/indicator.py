# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 11:07:46 2019

@author: chris
"""

import inspect
from ..utils import lower_column_headers
from ...plot.utils import initialize_figure, lower_column_headers
import numpy as np

class IndicatorBase:

    function = lambda x,y:x+1 # placeholder function
    DATAFRAMEKEYS = ("open", "high", "low", "close", "volume")

    @staticmethod
    def read_parameters_and_arguments(function):

        inspection = inspect.getfullargspec(function)
        defaults = inspection.defaults
        data_frame_args = []
        parameters = {}
        counter = 0

        for arg in inspection.args:
            if arg in Indicator.DATAFRAMEKEYS:
                data_frame_args.extend([arg])
            else:
                try:
                    parameters[arg] = defaults[counter]
                    counter +=1
                except:
                    raise Exception("input function does not contain key word arguments")
        return data_frame_args, parameters

    def __call__(self, dataframe):
        dataframe = lower_column_headers(dataframe)
        return self.function(
            *[dataframe[key] for key in self.data_frame_args],
            **self.parameters
        )

    def plot(self, dataframe, fig=None, **kwargs):
        p = initialize_figure(fig)
        dataframe = lower_column_headers(dataframe)

        p.line(
            dataframe["datetime"], self(dataframe)
        )
        return p

    @classmethod
    def random_initialization(cls, function, scale_default=3):
        _, parameters = cls.read_parameters_and_arguments(function)
        randomly_initializable = {}

        for key, value in parameters:
            if isinstance(value, int):
                randomly_initializable[key] = \
                    np.random.randint(1, int(value*scale_default))
            if isinstance(value, float):
                randomly_initializable[key] = \
                    np.random.randint(1, float(value*scale_default))

        return cls(function, **randomly_initializable)

class Indicator(IndicatorBase):
    """Indicator

    Arguments:
        the input to this class is an indicator function
        of form function({open/high/low/close}, **kwargs).
        Parameters are stored within the object for fine tuning.
        The resulting object contains a call function which
        accepts a dataframe.

    """
    def __init__(self, function, **kwargs):
        self.function = function
        assert inspect.isfunction(function), "input indicator must be a function"
        self.data_frame_args, self.parameters = self.read_parameters_and_arguments(function)
        allowed_keys = self.parameters.keys()
        for key, value in kwargs.items():
            if key in allowed_keys:
                self.parameters[key] = value
