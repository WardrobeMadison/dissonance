from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from ..analysis_functions import hill
from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


class ChirpEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.holdingpotential = epochgrp.attrs.get("holdingpotential")
        self.backgroundval = epochgrp.attrs.get("backgroundval")
        self.contrastmax = epochgrp.attrs.get("contrastmax")
        self.backgroundintensity = epochgrp.attrs.get("backgroundintensity")
        self.contrastfrequency = epochgrp.attrs.get("contrastfrequency")
        self.contrastmin = epochgrp.attrs.get("contrastmin")
        self.contrasttime = epochgrp.attrs.get("contrasttime")
        self.frequencycontrast = epochgrp.attrs.get("frequencycontrast")
        self.frequencymax = epochgrp.attrs.get("frequencymax")
        self.frequencymin = epochgrp.attrs.get("frequencymin")
        self.frequencytime = epochgrp.attrs.get("frequencytime")
        self.intertime = epochgrp.attrs.get("intertime")
        self.stepcontrast = epochgrp.attrs.get("stepcontrast")
        self.steptime = epochgrp.attrs.get("steptime")
        self.led = epochgrp.attrs.get("led")

    @property
    def type(self) -> str:
        return "ChirpTrace"


class ChirpEpochs(EpochBlock):

    type = "chirpepochs"

    def __init__(self, epochs: List[ChirpEpoch]):
        super().__init__(epochs)
        self.holdingpotential = epochs[0].holdingpotential
        self.backgroundval = epochs[0].backgroundval

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
