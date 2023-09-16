# https://github.com/sinha-lab-org/SymphonyAnalysis/blob/361cab9c7bd90b33317b0e63ad87aeeca210a6fd/core/%2Bstimuli/%2Bgenerators/GaussianNoiseGeneratorV2.m
from .stimulus_generator import StimulusGenerator
import numpy as np
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

    def generate(self) -> np.ndarray:
        def timetopts(t): return (round(t / 1e3 * self.samplerate))
        prepts = timetopts(self.pretime)
        stimpts = timetopts(self.stimtime)
        tailpts = timetopts(self.tailtime)

        # % Initialize random number generator.
        with MatlabRNorm() as rnorm:
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
