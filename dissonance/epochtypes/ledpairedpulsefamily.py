from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from .baseepoch import EpochBlock, IEpoch


class LedPairedPulseFamilyEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):

        super().__init__(epochgrp)

        self.intime = epochgrp.attrs["intime"]
        self.intime2 = epochgrp.attrs["intime2"]
        self.intimeadditive = epochgrp.attrs["intimeadditive"]
        self.led = epochgrp.attrs["led"]
        self.lightmean = epochgrp.attrs["lightmean"]
        self.pretime = epochgrp.attrs["pretime"]
        self.lightamplitude1 = epochgrp.attrs["lightamplitude1"]
        self.lightamplitude2 = epochgrp.attrs["lightamplitude2"]
        self.stimtime1 = epochgrp.attrs["stimtime1"]
        self.stimtime2 = epochgrp.attrs["stimtime2"]
        self.tailtime = epochgrp.attrs["tailtime"]

        # NOTE DO I NEED THESE
        self.holdingpotential = epochgrp.attrs.get("holdingpotential")
        self.backgroundval = epochgrp.attrs.get("backgroundval")

    @property
    def trace(self):
        vals = self._response_ds[:]
        return vals - np.mean(vals[: int(self.pretime)])

    @property
    def type(self) -> str:
        return "LedPairedPulseFamilyTrace"

    @property
    def g_ratio(self) -> float:
        return (self.peak2 - self.peak1) / self.peak2 + 1

    @property
    def peak1(self) -> float:
        vals = self.trace
        beg = int(self.pretime * 10)
        end = int(self.pretime + self.stimtime1 + self.intime2) * 10
        return np.min(vals[beg:end])

    @property
    def peak2(self) -> float:
        vals = self.trace
        end = int(self.pretime + self.stimtime1 + self.intime2) * 10
        return np.min(vals[end:])

    def __str__(self):
        return f"LedPairedPulseFamilyEpoch(cell_name={self.cellname}, start_date={self.startdate})"


class LedPairedPulseFamilyEpochs(EpochBlock):

    type = "ledpairedpulsefamilytraces"
    def __init__(self, epochs: List[LedPairedPulseFamilyEpoch]):
        super().__init__(epochs)

        
        self.holdingpotential = epochs[0].holdingpotential
        self.backgroundval = epochs[0].backgroundval

    @property
    def peak1(self) -> float:
        vals = self.trace
        beg = int(self.pretime * 10)
        end = int(self.pretime + self.stimtime1 + self.intime2) * 10
        return np.min(vals[beg:end])

    @property
    def peak2(self) -> float:
        vals = self.trace
        end = int(self.pretime + self.stimtime1 + self.intime2) * 10
        return np.min(vals[end:])

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
