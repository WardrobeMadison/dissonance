
import h5py
import numpy as np
import pandas as pd

from .baseepoch import IEpoch


class NoiseEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.stimparams = {key: val for key,
                        val in epochgrp['stimuli']["UV LED"].attrs.items()}

        self.amp = epochgrp.attrs["amp"]
        self.frequencycutoff = epochgrp.attrs["frequencycutoff"]
        self.interpulseinterval = epochgrp.attrs["interpulseinterval"]
        self.led = epochgrp.attrs["led"]
        self.lightmean = epochgrp.attrs["lightmean"]
        self.numberofaverages = epochgrp.attrs["numberofaverages"]
        self.numberoffilters = epochgrp.attrs["numberoffilters"]
        self.pretime = int(epochgrp.attrs["pretime"]*10)
        self.repeatsperstdv = epochgrp.attrs["repeatsperstdv"]
        self.samplerate = epochgrp.attrs["samplerate"]
        self.startstdv = epochgrp.attrs["startstdv"]
        self.stdvmultiples = epochgrp.attrs["stdvmultiples"]
        self.stdvmultiplier = epochgrp.attrs["stdvmultiplier"]
        self.stimtime = int(epochgrp.attrs["stimtime"]*10)
        self.tailtime = int(epochgrp.attrs["tailtime"]*10)
        self.userandomseed = epochgrp.attrs["userandomseed"]
        self.ndf = epochgrp.attrs["ndf"]
        self.seed = epochgrp.attrs["seed"]
        self.stdv = epochgrp.attrs["stdv"]

    @property
    def type(self):
        return "noisepoch"

    @property
    def trace(self):
        return self._response_ds[:] - np.mean(self._response_ds[:self.pretime])

    @property
    def stimulus(self):
        std = self.stimparams["stdev"]
        mean = self.stimparams["mean"]
        lower = self.stimparams["lowerlimit"]
        upper = self.stimparams["upperlimit"]
        seed = self.stimparams["seed"]

        np.random.seed(seed)

        # REVERSE ORDER TO MATCH MATLAB
        if self.stimparams["units"] == "_normalized_":
            stim = np.random.randn((1,len(self))).T * std + mean
            stim = np.clip(stim, lower, upper)
            return stim
        else:
            raise Exception(f"Don't know these units! {self.stimparams['units']}")

