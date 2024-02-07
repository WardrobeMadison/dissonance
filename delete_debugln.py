import numpy as np
from dissonance.analysis_functions.linear_nonlinear_model import LinearNonLinearModel

stimulus = np.load("stimulus.npy")
response = np.load("response.npy")

samplerate = 10000
pretime = 10000
tailtime = 10000
# plot_stimulus(stimulus, 0)

samplerate = 10000
pretime = 10000
tailtime = 10000
stimtime = 90000
frequencycutoff = 60
lightmean = 0.025
numberofaverages = 15

LinearNonLinearModel(
    stimulus,
    response,
    samplerate,
    pretime,
    tailtime,
    stimtime,
    frequencycutoff,
    lightmean,
    numberofaverages,
)
