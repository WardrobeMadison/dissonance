from typing import List
import numpy as np
from ..analysis_functions.psth import calculate_psth
from ..analysis_functions import hill
import h5py
from scipy.stats import sem

from .baseepoch import EpochBlock, IEpoch


class LedPairedSquareWavePulseEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.first_wave_contrast = epochgrp.attrs["firstWaveContrast"]
        self.first_wave_frequency = epochgrp.attrs["firstWaveFrequency"]
        self.first_wave_time = epochgrp.attrs["firstWaveTime"]
        self.intime = epochgrp.attrs["inTime"],
        self.interpulse_interval = epochgrp.attrs["interpulseInterval"]
        self.number_of_averages = epochgrp.attrs["numberOfAverages"]
        self.second_wave_contrast = epochgrp.attrs["secondWaveContrast"]
        self.second_wave_frequency = epochgrp.attrs["secondWaveFrequency"]
        self.second_wave_time = epochgrp.attrs["secondWaveTime"]

    @property
    def trace(self):
        vals = self._response_ds[:]
        return vals

    @property
    def type(self) -> str:
        return "LedPairedSquareWavePulseTrace"




class LedPairedSquareWavePulseEpochs(EpochBlock):

    type = "ledpairedsquarewavepulseepochs"

    def __init__(self, epochs: List[LedPairedSquareWavePulseEpoch]):
        super().__init__(epochs)

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
