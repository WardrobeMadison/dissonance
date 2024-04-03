from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from ..analysis_functions import hill
from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


class LedPairedSineWavePulseEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.first_wave_contrast = epochgrp.attrs["first_wave_contrast"]
        self.first_wave_frequency = epochgrp.attrs["first_wave_frequency"]
        self.first_wave_time = epochgrp.attrs["first_wave_time"]
        self.second_wave_contrast = epochgrp.attrs["second_wave_contrast"]
        self.second_wave_frequency = epochgrp.attrs["second_wave_frequency"]
        self.second_wave_time = epochgrp.attrs["second_wave_time"]

    @property
    def trace(self):
        vals = self._response_ds[:]
        # baseline subtracted
        vals = vals - np.mean(vals[: int(self.pretime)])
        return vals

    @property
    def type(self) -> str:
        return "LedPairedSineWavePulseTrace"


class LedPairedSineWavePulseEpochs(EpochBlock):

    type = "ledpairedsinewavepulseepochs"

    def __init__(self, epochs: List[LedPairedSineWavePulseEpoch]):
        super().__init__(epochs)

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
