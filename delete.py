import numpy as np

from dissonance import io
from dissonance.analysis_functions.linear_nonlinear_model import \
    LinearNonLinearModel
from dissonance.stimulus.matlab_random_numbers import MatlabRNorm


def read_spike_data():
    filterfilepath = None
    folders = [
        "GG2 KO",
    ]
    filters = dict(protocolname="LedNoiseFamily")

    paramnames = [
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "tracetype",
        "backgroundval",
        "lightmean",
        "startdate",
        "holdingpotential",
    ]
    dr = io.DissonanceReader.from_folders(folders)
    ef = dr.to_epoch_table(paramnames, filterpath=filterfilepath, filters=filters, nprocesses=1)
    return ef


df = read_spike_data()


# %%
epochs = df.loc[df.lightmean == 0.025, "epoch"].values

generators = [LedNoiseStimulusGenerator.from_epoch(epoch) for epoch in epochs]
responses = np.array([epoch.trace for epoch in epochs])

with MatlabRNorm() as rnorm:
    stimuli = np.array([gen.generate(rnorm) for gen in generators])

np.save("stimulus.npy", stimuli)
np.save("response.npy", responses)


samplerate = 10000
pretime = 1000
tailtime = 1000
stimtime = 9000
frequencycutoff = 60
lightmean = 0.025
numberofaverages = 15

# %%
LinearNonLinearModel(
    stimulus,
    epoch.trace,
    epoch.samplerate,
    epoch.pretime,
    epoch.tailtime,
    epoch.stimtime,
    epoch.frequencycutoff,
    epoch.lightmean,
    epoch.numberofaverages,
)
