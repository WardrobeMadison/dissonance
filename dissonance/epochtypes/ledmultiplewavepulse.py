from collections import defaultdict
from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from ..analysis_functions import hill
from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


class LedMultipleWavePulseEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.in_times = epochgrp.attrs["in_times"]
        self.led = epochgrp.attrs["led"]
        self.light_mean = epochgrp.attrs["lightmean"]
        self.pre_time = epochgrp.attrs["pretime"]
        self.tail_time = epochgrp.attrs["tailtime"]
        self.wave_contrasts = epochgrp.attrs["wave_contrasts"]
        self.wave_frequencies = epochgrp.attrs["wave_frequencies"]
        self.wave_times = epochgrp.attrs["wave_times"]
        self.wave_types = epochgrp.attrs["wave_types"]

        # NOTE assuming there is only UV LED
        self.stimulus = dict()
        for key, paramval in epochgrp["stimuli"]["UV LED"]:
            self.stimulus[key] = paramval

    @property
    def peaks(self):
        firstrace = self.trace[self.step_pre : self.first_window]
        secondtrace = self.trace[self.first_window : self.second_window]

        firstpeak = np.min(firstrace)
        secondpeak = np.min(secondtrace)
        return firstpeak, secondpeak

    @property
    def peak_ratio(self):
        firstpeak, secondpeak = self.peaks
        return firstpeak / secondpeak

    @property
    def trace(self):
        vals = self._response_ds[:]
        return vals - np.mean(vals[: int(self.pretime)])

    @property
    def type(self) -> str:
        return "ledmultiplewavepulseepoch"


class LedMultipleWavePulseEpochs(EpochBlock):

    type = "ledmultiplewavepulseepochs"

    def __init__(self, epochs: List[LedMultipleWavePulseEpoch]):
        super().__init__(epochs)

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
