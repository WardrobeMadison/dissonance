from typing import Dict, List

import h5py
import numpy as np

from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


class SpikeEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)
        self._spikegrp = epochgrp["Spikes"]
        self._psth = None
        self._binsize = 100

    @property
    def binsize(self):
        return self._binsize

    @binsize.setter
    def binsize(self, val):
        self._binsize = val

    @property
    def binsize_ms(self):
        return self.binsize / 10.0

    @property
    def spikes(self) -> np.array:
        return np.array(self._spikegrp[:], dtype=int)

    @property
    def psth(self) -> np.array:
        if self._psth is None:
            self._psth = calculate_psth(self)
        return self._psth

    @property
    def timetopeak(self) -> float:
        rng = self.peak_window_range
        return rng[0] // 100 + np.argmax(self.psth[rng[0] // 100 : rng[1] // 100])

    @property
    def peakamplitude(self) -> float:
        rng = self.peak_window_range
        return np.max(self.psth[rng[0] // 100 : rng[1] // 100])

    @property
    def timetopeaksec(self) -> float:
        return (self.timetopeak * 100 - self.pretime) / 10000

    @property
    def type(self) -> str:
        return "spiketrace"


class SpikeEpochs(EpochBlock):

    type = "spiketrace"

    def __init__(self, traces: List[IEpoch]):
        super().__init__(traces)
        self._psth: np.array = None
        self._psths: np.array = None
        self._hillfit: np.array = None
        self.rng = traces[0].peak_window_range

    @property
    def psth(self):
        if self._psth is None:
            self._psth = np.mean(self.psths, axis=0)
        return self._psth

    @property
    def psths(self) -> np.array:
        inc = 100
        if self._psths is None:
            self._psths = []
            for trace in self._epochs:
                if len(trace.psth) > 0 and trace.psth is not None:
                    cpsth = np.pad(trace.psth, (0, int(self.trace_len // inc - len(trace.psth))))
                    self._psths.append(cpsth)
        return np.array(self._psths, dtype=float)

    @property
    def timetopeak(self) -> float:
        return self.rng[0] // 100 + np.argmax(self.psth[self.rng[0] // 100 : self.rng[1] // 100])

    @property
    def peakamplitude(self) -> float:
        return np.max(self.psth[self.rng[0] // 100 : self.rng[1] // 100])

    @property
    def timetopeaksec(self) -> float:
        self.pretime = self.epochs[0].pretime
        return (self.timetopeak * 100 - self.pretime) / 10000
