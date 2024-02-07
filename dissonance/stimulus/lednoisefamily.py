# https://github.com/sinha-lab-org/SymphonyAnalysis/blob/361cab9c7bd90b33317b0e63ad87aeeca210a6fd/core/%2Bstimuli/%2Bgenerators/GaussianNoiseGeneratorV2.m
import numpy as np
from .stimulus_generator import StimulusGenerator
import matplotlib.pyplot as plt
import numpy as np
from dissonance.epochtypes.noiseepoch import NoiseEpoch
from scipy.fftpack import fft, ifft

from .matlab_random_numbers import MatlabRNorm


class LedNoiseStimulusGenerator(StimulusGenerator):
    def __init__(self,
                 freqcutoff: float,
                 inverted: float,
                 mean: float,
                 samplerate: float,
                 stdev: float,
                 pre_time: float,
                 stim_time: float,
                 tail_time: float,
                 units: float,
                 seed: int,
                 numfilters: int = 0,
                 upperlimit: float = np.inf,
                 lowerlimit: float = -np.inf,
                 ):

        self.freqcutoff = freqcutoff
        self.inverted = inverted
        self.lowerlimit = lowerlimit
        self.mean = mean
        self.numfilters = numfilters
        self.pretime = pre_time
        self.samplerate = samplerate
        self.seed = seed
        self.stdev = stdev
        self.stimtime = stim_time
        self.tailtime = tail_time
        self.units = units
        self.upperlimit = upperlimit

    def __len__(self):
        return self.preTime + self.stimTime + self.tailTime

    @classmethod
    def from_epoch(cls, epoch: NoiseEpoch):
        return LedNoiseStimulusGenerator(
            freqcutoff= epoch.frequencycutoff,
            inverted=epoch.stimparams["inverted"],
            mean= epoch.lightmean,
            samplerate= epoch.samplerate,
            stdev= epoch.stdv,
            pre_time= epoch.pretime,
            stim_time= epoch.stimtime,
            tail_time= epoch.tailtime,
            units= epoch.stimparams["units"] == "_normalized_",
            seed= epoch.seed,
            numfilters= epoch.numberoffilters,
            upperlimit= epoch.stimparams["upperlimit"],
            lowerlimit= epoch.stimparams["lowerlimit"],
        )

    def generate(self, rnorm = None) -> np.ndarray:
        prepts = self.pretime
        stimpts = self.stimtime
        tailpts = self.tailtime

        # % Initialize random number generator.
        if rnorm is None:
            with MatlabRNorm() as rnorm:
                noisetime = self.stdev * rnorm.sample(int(self.seed), 1, stimpts)
        else:
            noisetime = self.stdev * rnorm.sample(int(self.seed), 1, stimpts)

        # % To frequency domain.
        noisefreq = fft(noisetime)

        # % The filter will change based on whether or not there are an even or odd number of points.
        freqstep = self.samplerate / stimpts
        if stimpts % 2 == 0:
            # % Construct the filter.
            frequencies = np.arange(stimpts / 2+1) * freqstep
            onesidedfilter = 1 / \
                (1 + (frequencies / self.freqcutoff)**(2 * self.numfilters))
            filter = np.append(onesidedfilter, np.flip(onesidedfilter[1:-1]))
        else:
            # % Construct the filter.
            frequencies = np.arange((stimpts-1) / 2 + 1) * freqstep
            onesidedfilter = 1 / \
                (1 + (frequencies / self.freqcutoff) ** (2 * self.numfilters))
            filter = np.append(onesidedfilter, np.flip(onesidedfilter[1:]))

        # % Figure out factor by which filter will alter st dev - in the frequency domain, values should be
        # % proportional to standard deviation of each independent sinusoidal component, but it is the variances of
        # % these sinusoidal components that add to give the final variance, therefore, one needs to consider how the
        # % filter values will affect the variances; note that the first value of the filter is omitted, because the
        # % first value of the fft is the mean, and therefore shouldn't contribute to the variance/standard deviation
        # % in the time domain.
        filterFactor = np.sqrt(filter[1:] @ filter[1:].T / (stimpts - 1))

        # % Filter in freq domain.
        noisefreq = noisefreq * filter

        # % Set first value of fft (i.e., mean in time domain) to 0.
        noisefreq[0, 0] = 0

        # % Go back to time domain.
        noisetime = ifft(noisefreq)

        # % FilterFactor should represent how much the filter is expected to affect the standard deviation in the time
        # % domain, use it to rescale the noise.
        noisetime = noisetime / filterFactor

        noisetime = noisetime.real


        # % Flip if specified.
        if self.inverted:
            noisetime = -noisetime

        data = np.ones(prepts + stimpts + tailpts) * self.mean
        data[prepts:prepts + stimpts] = noisetime + self.mean

        data = np.clip(data, self.lowerlimit, self.upperlimit)

        return data

def plot_stimulus(Y, seed):
    X = np.arange(Y.shape[0]) / 1e4

    std = np.std(Y)
    mean = np.mean(Y)

    fig, ax = plt.subplots()
    ax.plot(X, Y, c="purple", alpha=0.35)
    ax.set_title(f"N({mean:.2f}, {std:2f}) with seed={seed}")
    fig.show()
    return fig

