import h5py

from dissonance.epochtypes.expandingspots import ExpandingSpotsEpoch

from .adaptingsteps import AdaptingStepsEpoch
from .chirpepoch import ChirpEpoch
from .ledpairedpulsefamily import LedPairedPulseFamilyEpoch
from .ledpairedsinewavepulse import LedPairedSineWavePulseEpoch, LedPairedSineWavePulseSpikeEpoch, LedPairedSineWavePulseWholeEpoch
from .ledpulse import LedPulseSpikeEpoch, LedPulseWholeEpoch
from .ledpulsefamily import LedPulseFamilySpikeEpoch, LedPulseFamilyWholeEpoch
from .noiseepoch import NoiseEpoch
from .sacaadeepoch import SaccadeSpikeEpoch, SaccadeWholeEpoch
from .ledmultiplewavepulse import LedMultipleWavePulseEpoch, LedMultipleWavePulseEpochs

EpochType = (
    LedPulseSpikeEpoch
    | LedPulseWholeEpoch
    | LedPulseFamilySpikeEpoch
    | LedPulseFamilyWholeEpoch
    | SaccadeSpikeEpoch
    | SaccadeWholeEpoch
    | NoiseEpoch
    | ChirpEpoch
    | LedPairedPulseFamilyEpoch
    | AdaptingStepsEpoch
    | LedPairedSineWavePulseSpikeEpoch
    | LedPairedSineWavePulseWholeEpoch
    | LedMultipleWavePulseEpoch
)


def epoch_factory(epochgrp: h5py.Group) -> EpochType:
    protocolname = epochgrp.attrs["protocolname"]
    if protocolname == "LedNoiseFamily":
        return NoiseEpoch(epochgrp)

    elif protocolname == "AdaptingSteps":
        return AdaptingStepsEpoch(epochgrp)

    elif protocolname in ["LedPairedPulseFamily", "LedPairedPulseFamilyOriginal"]:
        return LedPairedPulseFamilyEpoch(epochgrp)

    elif protocolname == "ChirpStimulusLED":
        return ChirpEpoch(epochgrp)

    elif protocolname == "ExpandingSpots":
        return ExpandingSpotsEpoch(epochgrp)

    elif protocolname == "SaccadeTrajectory2":
        tracetype = epochgrp.attrs["tracetype"]
        if tracetype == "spiketrace":
            return SaccadeSpikeEpoch(epochgrp)
        elif tracetype == "wholetrace":
            return SaccadeWholeEpoch(epochgrp)

    elif protocolname in "LedPulseFamily":
        tracetype = epochgrp.attrs["tracetype"]
        if tracetype == "spiketrace":
            return LedPulseFamilySpikeEpoch(epochgrp)
        elif tracetype == "wholetrace":
            return LedPulseFamilyWholeEpoch(epochgrp)

    elif protocolname == "LedPulse":
        tracetype = epochgrp.attrs["tracetype"]
        if tracetype == "spiketrace":
            return LedPulseSpikeEpoch(epochgrp)
        elif tracetype == "wholetrace":
            return LedPulseWholeEpoch(epochgrp)

    elif protocolname in ("LedPairedSineWavePulse",):
        tracetype = epochgrp.attrs["tracetype"]
        if tracetype == "spiketrace":
            return LedPairedSineWavePulseSpikeEpoch(epochgrp)
        elif tracetype == "wholetrace":
            return LedPairedSineWavePulseWholeEpoch(epochgrp)

    elif protocolname == "LedMultipleWavePulse":
        return LedMultipleWavePulseEpoch(epochgrp)

    else:
        raise NotImplementedError(f"Trace type not yet specified for {epochgrp}")
