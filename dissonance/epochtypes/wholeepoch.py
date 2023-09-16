from functools import cached_property
from typing import List

import h5py
import numpy as np
import pandas as pd
from scipy.stats import sem

from ..analysis_functions import hill
from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


def calc_width_at_half_max(values, holdingpotential):
    """Width at half max (actually half min since data should be negative"""
    if holdingpotential == "inhibition":
        ttp = np.argmax(values)
        halfmax = np.max(values) / 2.0
    else:
        ttp = np.argmin(values)
        halfmax = np.min(values) / 2.0

    if halfmax < 0:
        start = ttp - np.argmax(values[ttp::-1] > halfmax)
        end = np.argmax(values[ttp:] > halfmax) + ttp
    else:
        start = ttp - np.argmax(values[:ttp:-1] < halfmax)
        end = np.argmax(values[ttp:] < halfmax) + ttp

    return end-start, (int(start),int(end))


class WholeEpoch(IEpoch):

    def __init__(self, epochgrp:h5py.Group):

        super().__init__(epochgrp)
        self.holdingpotential = epochgrp.attrs.get("holdingpotential")
        self.backgroundval = epochgrp.attrs.get("backgroundval")
        self.exclude_timesteps = epochgrp.attrs.get("exclude_timesteps")
        self._widthathalfmax = None
        self._timetopeak = None
        self._peakamplitude = None
        self._widthrange = None

    @property
    def trace(self):
        vals = self._response_ds[:] 
        return vals - np.mean(vals[:int(self.pretime)])

    @cached_property
    def timetopeak(self) -> float:
        rng = self.peak_window_range
        if self._timetopeak is None:
            if (self.holdingpotential == "inhibition") or (self.lightamplitude < 0):
                self._timetopeak  = rng[0] + np.argmax(self.trace[rng[0]:rng[1]])
            else: 
                self._timetopeak  = rng[0] + np.argmin(self.trace[rng[0]:rng[1]])
        return self._timetopeak

    @cached_property
    def widthrange(self) -> float:
        if self._widthrange is None:
            # set this property to set range as well
            self.width_at_half_max
        return self._widthrange

    @cached_property
    def peakamplitude(self) -> float:
        rng = self.peak_window_range
        if self._peakamplitude is None:
            if (self.holdingpotential == "inhibition") or (self.lightamplitude < 0):
                self._peakamplitude  = np.max(self.trace[rng[0]:rng[1]])
            else: 
                # FIND MIN WHEN EXCLUDING TIMESTEPS
                if self.has_spikes:
                    self._peakamplitude  = self.interpolate["y_interpolated"].min()
                else:
                    self._peakamplitude  = np.min(self.trace[rng[0]:rng[1]])
        return self._peakamplitude

    @cached_property
    def width_at_half_max(self) -> float:
        rng = self.peak_window_range
        if self._widthathalfmax is None:
            self._widthathalfmax, self._widthrange = calc_width_at_half_max(self.trace[rng[0]:rng[1]], self.holdingpotential)
            self._widthrange = (rng[0] + self._widthrange[0], rng[0] + self._widthrange[1])
        return self._widthathalfmax

    @property
    def type(self) -> str:
        return "WholeTrace"

    @cached_property
    def flashintensity(self) -> float:
        return ((self.lightamplitude  + self.lightmean) * (self.stimtime / 10000))

    @cached_property
    def gain(self) -> float:
        return self.peakamplitude / self.flashintensity

    @cached_property
    def crf_value(self) -> float:
        rng = self.peak_window_range
        if "ON" in self.celltype and self.lightamplitude < 0:
            return np.max(self.trace[rng[0]:rng[1]])
        else:
            return self.peakamplitude
    
    @cached_property
    def timetopeaksec(self) -> float:
        return (self.timetopeak  - self.pretime) / 10000

    @cached_property
    def has_spikes(self) -> bool:
      # return self.trace.min() / self.trace.mean() > 8
        return False

    #@cached_property
    #def interpolated(self) -> np.ndarray:
    #    df = filter_peaky_things(self.trace)
    #    return df["y_interpolated"].values

class WholeEpochs(EpochBlock):

    type = "wholetrace"

    def __init__(self, epochs: List[WholeEpoch]):
        super().__init__(epochs)
        self.holdingpotential = epochs[0].holdingpotential
        self.backgroundval = epochs[0].backgroundval
        self._widthathalfmax = None
        self._widthrange = None
        self._timetopeak = None
        self._peakamplitude = None
        
        # ASSUME THE SAME FOR ALL UNDERYLHIN
        self.peak_window_range = epochs[0].peak_window_range
        self.flashintensity = epochs[0].flashintensity

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)

    @property
    def width_at_half_max(self) -> float:
        rng = self.peak_window_range
        if self._widthathalfmax is None:
            self._widthathalfmax, self._widthrange = calc_width_at_half_max(self.trace[rng[0]:rng[1]], self.holdingpotential)
            self._widthrange = (rng[0] + self._widthrange[0], rng[0] + self._widthrange[1])
        return self._widthathalfmax

    @property
    def timetopeak(self) -> float:
        rng = self.peak_window_range
        if self._timetopeak is None:
            lightamp = self._epochs[0].lightamplitude
            if (self.holdingpotential == "inhibition") or (lightamp < 0):
                self._timetopeak  = rng[0] + np.argmax(self.trace[rng[0]:rng[1]])
            else: 
                self._timetopeak  = rng[0] + np.argmin(self.trace[rng[0]:rng[1]])
        return self._timetopeak

    @property
    def widthrange(self) -> float:
        if self._widthrange is None:
            # set this property to set range as well
            self.width_at_half_max
        return self._widthrange

    @property
    def peakamplitude(self) -> float:
        rng = self.peak_window_range
        if self._peakamplitude is None:
            lightamp = self._epochs[0].lightamplitude
            if (self.holdingpotential == "inhibition") or (lightamp < 0):
                self._peakamplitude  = np.max(self.trace[rng[0]:rng[1]])
            else: 
                self._peakamplitude  = np.min(self.trace[rng[0]:rng[1]])
        return self._peakamplitude

    @property
    def gain(self) -> float:
        return self.peakamplitude / self.flashintensity

    @property
    def crf_value(self) -> float:
        rng = self.peak_window_range

        lightamp = self._epochs[0].lightamplitude
        celltype = self._epochs[0].celltype

        if "ON" in celltype and lightamp < 0:
            return np.max(self.trace[rng[0]:rng[1]])
        else:
            return self.peakamplitude

    @property
    def timetopeaksec(self) -> float:
        self.pretime = self.epochs[0].pretime
        return (self.timetopeak - self.pretime) / 10000

           
