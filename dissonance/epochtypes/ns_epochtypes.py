from collections import defaultdict

import pandas as pd

from . import adaptingsteps as ae
from . import chirpepoch as ce
from . import expandingspots as es
from . import ledpairedpulsefamily as wt
from . import ledpairedsinewavepulse as wp
from . import ledpulse as st
from . import ledpulsefamily as fa
from . import sacaadeepoch as sa
from . import ledmultiplewavepulse as lm


def groupby(frame: pd.DataFrame, grpkeys) -> pd.DataFrame:
    """
    Convert Traces to table with Epochs grouped by grpkeys
    """
    defaultdict(list)
    epochtype = type(frame.epoch.iloc[0])  # ASSUME SINGLE TYPE PER LIST

    if epochtype == wt.LedPairedPulseFamilyEpoch:
        types = wt.LedPairedPulseFamilyEpochs

    elif epochtype == st.LedPulseSpikeEpoch:
        types = st.LedPulseSpikeEpochs
    elif epochtype == st.LedPulseWholeEpoch:
        types = st.LedPulseWholeEpochs

    elif epochtype == fa.LedPulseFamilySpikeEpoch:
        types = fa.LedPulseFamilySpikeEpochs
    elif epochtype == fa.LedPulseFamilyWholeEpoch:
        types = fa.LedPulseFamilyWholeEpochs

    elif epochtype == sa.SaccadeSpikeEpoch:
        types = sa.SaccadeSpikeEpochs
    elif epochtype == sa.SaccadeWholeEpoch:
        types = sa.SaccadeWholeEpochs

    elif epochtype == ce.ChirpEpoch:
        types = ce.ChirpEpochs

    elif epochtype == ae.AdaptingStepsEpoch:
        types = ae.AdpatingStepsEpochs

    elif epochtype == es.ExpandingSpotsEpoch:
        types = es.ExpandingsSpotsEpochs

    elif epochtype == wp.LedPairedSineWavePulseSpikeEpoch:
        types = wp.LedPairedSineWavePulseSpikeEpochs
    elif epochtype == wp.LedPairedSineWavePulseWholeEpoch:
        types = wp.LedPairedSineWavePulseWholeEpochs

    elif epochtype == lm.LedMultipleWavePulseEpoch:
        types = lm.LedMultipleWavePulseEpochs
    else:
        raise NotImplementedError()

    data = []
    for key, grp in frame.groupby(grpkeys):
        data.append([*key, types(grp["epoch"].values)])

    return pd.DataFrame(columns=[*grpkeys, "epoch"], data=data)


def filter(epochs, **kwargs):
    out = []
    for epoch in epochs:
        condition = all([getattr(epoch, key) == val for key, val in kwargs.items()])
        if condition:
            out.append(epoch)
    tracetype = type(epochs)
    return tracetype(out)
