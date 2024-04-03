import h5py

from .base_spike_epoch import SpikeEpoch, SpikeEpochs
from .base_whole_epoch import WholeEpoch, WholeEpochs


class LedPulseFamilySpikeEpoch(SpikeEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)


class LedPulseFamilySpikeEpochs(SpikeEpochs):

    def __init__(self, traces: list[LedPulseFamilySpikeEpoch]):
        super().__init__(traces)


class LedPulseFamilyWholeEpoch(WholeEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)


class LedPulseFamilyWholeEpochs(WholeEpochs):

    def __init__(self, traces: list[LedPulseFamilyWholeEpoch]):
        super().__init__(traces)
