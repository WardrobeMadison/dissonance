import h5py

from dissonance.epochtypes.expandingspots import ExpandingSpotsEpoch

from .spikeepoch import SpikeEpoch
from .wholeepoch import WholeEpoch
from .noiseepoch import NoiseEpoch
from .sacaadeepoch import SaccadeEpoch
from .chirpepoch import ChirpEpoch
from .ledpairedpulsefamily import LedPairedPulseFamilyEpoch
from .adaptingsteps import AdaptingStepsEpoch
from .ledpairedsinewavepulse import LedPairedSineWavePulseEpoch

EpochType = SpikeEpoch | WholeEpoch | NoiseEpoch | SaccadeEpoch | ChirpEpoch | LedPairedPulseFamilyEpoch | AdaptingStepsEpoch


def epoch_factory(epochgrp: h5py.Group) -> EpochType:
    protocolname = epochgrp.attrs["protocolname"]
    if protocolname == "LedNoiseFamily":
        return NoiseEpoch(epochgrp)
    elif protocolname == "SaccadeTrajectory2":
        return SaccadeEpoch(epochgrp)
    elif protocolname == "AdaptingSteps":
        return AdaptingStepsEpoch(epochgrp)
    elif protocolname in ["LedPairedPulseFamily", "LedPairedPulseFamilyOriginal"]:
        return LedPairedPulseFamilyEpoch(epochgrp)
    elif protocolname == "ChirpStimulusLED":
        return ChirpEpoch(epochgrp)
    elif protocolname == "ExpandingSpots":
        return ExpandingSpotsEpoch(epochgrp)
    elif protocolname in ["LedPulse", "LedPulseFamily"]:
        tracetype = epochgrp.attrs["tracetype"]
        if tracetype == "spiketrace":
            return SpikeEpoch(epochgrp)
        elif tracetype == "wholetrace":
            return WholeEpoch(epochgrp)
    elif protocolname in ("LedPairedSineWavePulse", ):
        return LedPairedSineWavePulseEpoch(epochgrp)
    else:
        raise NotImplementedError(f"Trace type not yet specified for {epochgrp}")
