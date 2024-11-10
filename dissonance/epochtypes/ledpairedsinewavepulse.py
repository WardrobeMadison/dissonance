#type: ignore
from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from dissonance.epochtypes.base_spike_epoch import SpikeEpoch, SpikeEpochs
from dissonance.epochtypes.base_whole_epoch import WholeEpoch, WholeEpochs


class LedPairedSineWavePulseEpoch:

    def __init__(self, epochgrp: h5py.Group):
        self.first_wave_contrast = epochgrp.attrs["first_wave_contrast"]
        self.first_wave_frequency = epochgrp.attrs["first_wave_frequency"]
        self.first_wave_time = epochgrp.attrs["first_wave_time"]
        self.second_wave_contrast = epochgrp.attrs["second_wave_contrast"]
        self.second_wave_frequency = epochgrp.attrs["second_wave_frequency"]
        self.second_wave_time = epochgrp.attrs["second_wave_time"]


class LedPairedSineWavePulseSpikeEpoch(SpikeEpoch, LedPairedSineWavePulseEpoch):
    def __init__(self, epochgrp: h5py.Group):
        SpikeEpoch.__init__(self, epochgrp)
        LedPairedSineWavePulseEpoch.__init__(self, epochgrp)

class LedPairedSineWavePulseWholeEpoch(WholeEpoch, LedPairedSineWavePulseEpoch):
    def __init__(self, epochgrp: h5py.Group):
        WholeEpoch.__init__( self, epochgrp)
        LedPairedSineWavePulseEpoch.__init__(self, epochgrp)


class LedPairedSineWavePulseSpikeEpochs(SpikeEpochs):
    def __init__(self, traces: list[LedPairedSineWavePulseEpoch]):
        super().__init__(traces)

class LedPairedSineWavePulseWholeEpochs(WholeEpochs):
    def __init__(self, traces: list[LedPairedSineWavePulseEpoch]):
        super().__init__(traces)
