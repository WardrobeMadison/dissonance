from typing import List

import h5py
import numpy as np
from scipy.stats import sem

from ..analysis_functions import hill
from ..analysis_functions.psth import calculate_psth
from .baseepoch import EpochBlock, IEpoch


class AdaptingStepsEpoch(IEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)

        self.baseline_magnitude = epochgrp.attrs["baseline_magnitude"]
        self.step_magnitude = epochgrp.attrs["step_magnitude"]
        self.flash_duration = epochgrp.attrs["flash_duration"]

        self.fixed_pre_flash_amp = epochgrp.attrs["fixed_pre_flash_amp"]
        self.fixed_post_flash_amp = epochgrp.attrs["fixed_post_flash_amp"]
        self.fixed_step_flash_amp = epochgrp.attrs["fixed_step_flash_amp"]

        self.fixed_post_flash_time = epochgrp.attrs["fixed_post_flash_time"]
        self.fixed_pre_flash_time = epochgrp.attrs["fixed_pre_flash_time"]
        self.fixed_step_flash_time = epochgrp.attrs["fixed_step_flash_time"]

        self.step_stim = epochgrp.attrs["step_stim"]
        self.step_pre = epochgrp.attrs["step_pre"]
        self.step_tail = epochgrp.attrs["step_tail"]

        self.variable_flash_times = epochgrp.attrs["variable_flash_times"]
        self.variable_flash_time = epochgrp.attrs["variable_flash_time"]
        self.variable_post_flash_amp = epochgrp.attrs["variable_post_flash_amp"]
        self.variable_step_flash_amp = epochgrp.attrs["variable_step_flash_amp"]

        # self.stimulus = epochgrp["UV LED"]

        # self._stim_steps = defaultdict(dict)
        # for key, paramval in self.stimulus.attrs.items():
        #    ledname, param = key.splt("_")
        #    self._stim_steps[ledname][param] = paramval

    @property
    def stim_steps(self):
        return self._stim_steps

    @property
    def first_window(self):
        return int(self.step_pre) + int(self.fixed_step_flash_time)

    @property
    def second_window(self):
        return int(self.step_pre) + int(self.variable_step_flash_time)

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
        return vals

    @property
    def type(self) -> str:
        return "ApdatingStepTrace"

    @property
    def peaks(self): ...

    @property
    def peaks(self): ...


class AdpatingStepsEpochs(EpochBlock):

    type = "adaptingstepsepochs"

    def __init__(self, epochs: List[AdaptingStepsEpoch]):
        super().__init__(epochs)

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)
