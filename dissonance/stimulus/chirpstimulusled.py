import numpy as np

from ..epochtypes import ChirpEpoch, ChirpEpochs


class ChirpStimulusLED:

    def __init__(
        self,
        intertime,
        steptime,
        samplerate,
        backgroundintensity,
        frequencycontrast,
        frequencytime,
        frequencymin,
        frequencymax,
        contrastfrequency,
        stepcontrast,
        contrasttime,
        contrastmax,
        contrastmin,
    ):
        self.intertime = intertime
        self.steptime = steptime
        self.samplerate = samplerate
        self.backgroundintensity = backgroundintensity

        self.frequencycontrast = frequencycontrast
        self.frequencytime = frequencytime
        self.frequencymin = frequencymin
        self.frequencymax = frequencymax

        self.contrastfrequency = contrastfrequency
        self.stepcontrast = stepcontrast
        self.contrasttime = contrasttime
        self.contrastmax = contrastmax
        self.contrastmin = contrastmin

    @classmethod
    def from_epoch(cls, epoch: ChirpEpoch) -> "ChirpStimulusLED":
        return cls(
            epoch.intertime,
            epoch.steptime,
            epoch.samplerate,
            epoch.backgroundintensity,
            epoch.frequencycontrast,
            epoch.frequencytime,
            epoch.frequencymin,
            epoch.frequencymax,
            epoch.contrastfrequency,
            epoch.stepcontrast,
            epoch.contrasttime,
            epoch.contrastmax,
            epoch.contrastmin,
        )

    @classmethod
    def from_epochs(cls, epochs: ChirpEpochs) -> "ChirpStimulusLED":
        # assume t hey are all the same
        epoch: ChirpEpoch = epochs.epochs[0]
        return cls.from_epoch(epoch)

    @property
    def stimulus(self):
        return self._stim

    def timetopts(self, t):
        return round(t / 1e3 * self.samplerate)

    def ptstotime(self, p):
        return p / self.samplerate

    def generate(self):
        self._convert_inputs()
        self._init_stim_vector()
        self._calculate_deltas()
        self._generate_pretime()
        self._generate_frequency_sweep()
        self._generate_contrast_sweep()
        return self._stim

    def _calculate_deltas(self):
        # not sure why factor of 2 needed but gets frequencies right
        self.frequencydelta = (self.frequencymax - self.frequencymin) / self.freqpts / 2
        self.contrastdelta = (self.contrastmax - self.contrastmin) / self.contrastpts

    def _convert_inputs(self):
        tottime = self.intertime * 5 + self.steptime * 2 + self.frequencytime + self.contrasttime

        self.totpts = self.timetopts(tottime)

        self.interpts = self.timetopts(self.intertime)
        self.steppts = self.timetopts(self.steptime)
        self.freqpts = self.timetopts(self.frequencytime)
        self.contrastpts = self.timetopts(self.contrasttime)

    def _init_stim_vector(self):
        self._stim = np.ones(self.totpts)
        self._stim[:] = self.backgroundintensity

    def _generate_pretime(self):
        # increment and decrement steps
        self._stim[self.interpts + 1 : self.interpts + self.steppts] = (
            self._stim[self.interpts + 1 : self.interpts + self.steppts]
            + self.stepcontrast * self.backgroundintensity
        )
        self._stim[self.interpts * 2 + self.steppts + 1 : self.interpts * 2 + self.steppts * 2] = (
            self._stim[self.interpts * 2 + self.steppts + 1 : self.interpts * 2 + self.steppts * 2]
            - self.stepcontrast * self.backgroundintensity
        )

    @property
    def range_increment_step(self):
        return self.interpts + 1, self.interpts + self.steppts

    @property
    def range_decrement_steps(self):
        return self.interpts * 2 + self.steppts + 1, self.interpts * 2 + self.steppts * 2

    @property
    def range_freq_sweep(self):
        start = self.interpts * 3 + self.steppts * 2
        return start, start + self.freqpts

    @property
    def range_contrast_sweep(self):
        start = self.interpts * 4 + self.steppts * 2 + self.freqpts
        return start, start + self.contrastpts

    def _generate_frequency_sweep(self):
        start, _ = self.range_freq_sweep
        for t in np.arange(self.freqpts):
            self._stim[t + start] = (
                self.frequencycontrast
                * self.backgroundintensity
                * np.sin(2 * np.pi * self.ptstotime(t) * (self.frequencymin + self.frequencydelta * t))
                + self.backgroundintensity
            )

    def _generate_contrast_sweep(self):
        start, _ = self.range_contrast_sweep
        for t in np.arange(self.contrastpts):
            self._stim[t + start] = (
                self.contrastmin + t * self.contrastdelta
            ) * self.backgroundintensity * np.sin(
                2 * np.pi * self.ptstotime(t) * self.contrastfrequency
            ) + self.backgroundintensity
