from ...math import PolyfitSavgolFilter, find_min_from_gradients, ConstantPaddingSavgolFilter
from .. import dataFields
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.signal import savgol_filter

class PartialFilter:

    def __init__(self, window_length, polyorder):
        self.window_length = window_length
        self.polyorder = polyorder

    def __call__(self, signal):
        return savgol_filter(
            signal, self.window_length, self.polyorder
        )

class SavitzkyMin:

    def __init__(
        self, signalWindow, gradientWindow,
        signalPoly=3, gradientPoly=3, field="close",
        signalRetain=10, clip=500, mode="b"
    ):
        if mode.lower() == "a":
            self.signalFilter = PolyfitSavgolFilter(signalWindow, polyorder=signalPoly)
            self.gradientFilter = PolyfitSavgolFilter(gradientWindow, polyorder=gradientPoly)
        if mode.lower() == "b":
            self.signalFilter = ConstantPaddingSavgolFilter(
                signalWindow, polyorder=signalPoly)
            self.gradientFilter = ConstantPaddingSavgolFilter(
                gradientWindow, polyorder=gradientPoly)
        if mode.lower() == "c":
            self.signalFilter = PartialFilter(signalWindow, signalPoly)
            self.gradientFilter = PartialFilter(gradientWindow, gradientPoly)

        self.signalRetain = signalRetain
        assert field in dataFields.keys()
        self.field = field
        self.clip = clip

    def __call__(self, dohlcv):
        key = dataFields[self.field]
        desiredField = dohlcv[key]
        if len(dohlcv[0]) >= self.clip:
            clippedField = desiredField
        else:
            clippedField = desiredField[-self.clip:]
        filteredSignal = self.signalFilter(clippedField)
        grad = np.concatenate(
            [ [0,],np.diff(filteredSignal)]
        )
        filteredGrad = self.gradientFilter(grad)
        self.features = \
            find_min_from_gradients(filteredGrad) + (len(desiredField) - len(clippedField))
        return self.process(desiredField)

    def process(self, desiredField):
        if len(self.features):
            latestFeature = self.features[-1]
            if latestFeature >= (len(desiredField) - 1 - self.signalRetain):
                return True
        return False