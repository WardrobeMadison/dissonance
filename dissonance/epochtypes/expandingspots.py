from typing import List

import numpy as np

from dissonance.epochtypes.spikeepoch import SpikeEpoch, SpikeEpochs
from ..analysis_functions.psth import calculate_psth
from ..analysis_functions import hill
import h5py
from scipy.stats import sem

from .baseepoch import EpochBlock, IEpoch


class ExpandingSpotsEpoch(SpikeEpoch):

    def __init__(self, epochgrp: h5py.Group):
        super().__init__(epochgrp)
        
        self._spikegrp = epochgrp["Spikes"]
        self.current_spot_size = epochgrp.attrs["current_spot_size"]
        self.randomize_order = epochgrp.attrs["randomize_order"] 
        self.sample_rate = epochgrp.attrs["sample_rate"]  
        self.spot_intensity = epochgrp.attrs["spot_intensity"]  
        self.spot_sizes = epochgrp.attrs["spot_sizes"] 
        self.background_intensity = epochgrp.attrs["background_intensity"]

    @property
    def type(self) -> str:
        return "ExpandingSpotsTrace"

class ExpandingsSpotsEpochs(SpikeEpochs):

    type = "expandingspotsepochs"

    def __init__(self, epochs: List[ExpandingSpotsEpoch]):
        super().__init__(epochs)
