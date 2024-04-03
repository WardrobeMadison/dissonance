import h5py

from .base_spike_epoch import SpikeEpoch, SpikeEpochs
from .base_whole_epoch import WholeEpoch, WholeEpochs


class LedPulseSpikeEpoch(SpikeEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)


class LedPulseSpikeEpochs(SpikeEpochs):

    def __init__(self, traces: list[LedPulseSpikeEpoch]):
        super().__init__(traces)


class LedPulseWholeEpoch(WholeEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)


class LedPulseWholeEpochs(WholeEpochs):

    def __init__(self, traces: list[LedPulseWholeEpoch]):
        super().__init__(traces)
