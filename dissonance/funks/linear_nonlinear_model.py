import numpy as np
from scipy.fftpack import fft, ifft
from scipy.optimize import fmin
from scipy.stats import norm

from .liner_filter_finder import linear_filter_finder


class LinearNonLinearModel:

    def __init__(self, stimulus, response, samplerate,
                 prepoints, tailpoints, datapoints,
                 freqcutoff, lightmean, numbins):
        """Compute linear filter and static nonlinearity from LED Noise Family stimulus"""

        stimulus, lightmean, response = self.stage_inputs(
            stimulus, lightmean, prepoints)

        self.lf = LinearFilterModel(
            stimulus, response, prepoints, datapoints, tailpoints, samplerate, freqcutoff)

        self.nf = NonLinearModel(
            self.lf.prediction, response, prepoints, datapoints, tailpoints, numbins)

    def stage_inputs(self, stimulus, lightmean, prepoints, response):
        # get stimulus data
        # clip stimulus values at zero (can't have negative led output)
        stimulus[stimulus < 0] = 0
        # normalize to zero mean and units of contrast
        stimulus = (stimulus - lightmean) / lightmean

        # get response data, filter and baseline
        # subgtract baseline
        response = np.mean(np.mean(response[:, 1:prepoints]))

        numepochs = response.shape[0]

        return stimulus, response, numepochs


class LinearFilterModel:

    def __init__(self,
                 stimulus, response, prepoints, datapoints, tailpoints, samplerate, freqcutoff):

        self.calculate_filter(
            stimulus, response, prepoints, datapoints, tailpoints, samplerate, freqcutoff)

        self.measure(self.filter, samplerate)

        self.ampltude_spectrum_of_lin_filter(self.filter, samplerate)

    @property
    def ampspec_norm_mean(self):
        return self.binned_ampspec_mean / max(self.binned_ampspec_mean)

    @property
    def ampspec_norm_sem(self):
        return self.binned_ampspec_sem / max(self.binned_ampspec_mean)

    def calculate_filter(self, stimulus, response, prepoints, datapoints, tailpoints, samplerate, freqcutoff):
        """find linear filter and linear prediction from convolution of stimulus with linear filter"""
        self.filter = linear_filter_finder(
            stimulus[:, prepoints+1:datapoints-(tailpoints+1)],
            response[:, prepoints+1:datapoints-(tailpoints+1)],
            samplerate,
            freqcutoff)

        self.filter = (
            self.filter / np.std(self.filter, 0, 2)
            * np.mean(np.std(stimulus[:, prepoints+1:datapoints-(tailpoints+1)], 0, 2)))

        # linear prediction from convolution of stimulus with linear filter
        self.prediction = np.empty(
            stimulus[:, prepoints+1:datapoints-(tailpoints+1)].shape)
        self.prediction[:] = np.nan

        for ii in range(1, response.shape[0]):
            self.prediction[ii, :] = np.real(ifft(
                (fft(stimulus[ii, prepoints+1:datapoints-(tailpoints+1)]) * fft(self.filter))))

    def measure(self, linearfilter, samplerate):
        """ linear filter measurements (peak amplitudes, peak times, halfwidths) """
        self.inpeak = np.min(linearfilter[:, 1: (0.5*samplerate)])
        self.outpeak = np.max(linearfilter[:, 1: (0.5*samplerate)])

        self.time_inpeak = (linearfilter == self.inpeak) * \
            (1/samplerate)  # units of seconds
        self.time_outpeak = (linearfilter == self.outpeak)*(1/samplerate)

        # for on cells
        if abs(self.inpeak) >= abs(self.outpeak):
            halfpeak = self.inpeak * 0.5

            beforepeak = linearfilter

            beforepeak[:,  len(beforepeak), (np.floor(
                self.time_inpeak*samplerate)):] = np.nan
            halfpoint1 = [beforepeak > halfpeak][-1] + 1

            afterpeak = linearfilter
            afterpeak[:, 1: (np.floor(self.time_inpeak*samplerate))] = np.nan

            # units of seconds
            halfpoint2 = (afterpeak > halfpeak)[0] - 1
            self.halfwidth = (halfpoint2 - halfpoint1)*(1/samplerate)

        # off cells
        else:
            halfpeak = self.outpeak*0.5
            beforepeak = linearfilter
            beforepeak[:,  len(beforepeak): np.floor(
                self.time_outpeak*samplerate)] = np.nan

            halfpoint1 = (beforepeak < halfpeak)[-1] + 1
            afterpeak = linearfilter

            afterpeak[:, 1: np.floor(self.time_outpeak*samplerate)] = np.nan
            halfpoint2 = (afterpeak < halfpeak)[0] - 1
            self.halfwidth = (halfpoint2 - halfpoint1)*(1/samplerate)

    def ampltude_spectrum_of_lin_filter(self, linearfilter, samplerate):
        """ amplitude spectrum of lin filter """
        ft_filter = fft(linearfilter)
        # units correct? make sure to check this
        ampspec_filter = 2*abs(ft_filter)*(1/samplerate)/(len(ft_filter))

        nyquist = samplerate/2
        # note these are positive frequencies only
        self.freqaxis = np.arange(0, samplerate/(len(ft_filter)), nyquist)
        # ampspec_filter = ampspec_filter(1:length(freqaxis)); #truncate amp spectrum to positive frequencies only

        # bin
        ampspec_filter_row = ampspec_filter.reshape(1, linearfilter.shape[1])

        binlimits = np.linspace(min(self.freqaxis), max(
            self.freqaxis), nyquist)  # 1 hz bins
        numbinlimits = len(binlimits)-1
        self.ampspec_mean = np.zeros(1, numbinlimits)
        self.ampspec_sem = np.zeros(1, numbinlimits)
        self.freqaxis = np.zeros(1, numbinlimits)

        for ii in range(numbinlimits):
            indices = (self.freqaxis > binlimits(ii) &
                       self.freqaxis <= binlimits(ii+1))
            self.ampspec_mean[ii] = np.mean(ampspec_filter_row(indices))
            self.ampspec_sem[ii] = np.std(
                ampspec_filter_row(indices))/np.sqrt(len(indices))
            self.freqaxis[ii] = np.mean(self.freqaxis(indices))

        return self.ampspec_mean, self.ampspec_sem, self.freqaxis


class NonLinearModel:

    def __init__(self, linearprediction, response, prepoints, datapoints, tailpoints, numbins):

        self.linpred_mean, self.linpred_sem, self.responses_mean, self.responses_sem = (
            self.static_nonlinearity(linearprediction, response, prepoints, datapoints, tailpoints, numbins))
        self.mean, self.sem = self.fit_nonlinearity(
            self.linpred_mean, self.responses_mean)

        self.shift_upper = self.max(self.responses_mean)
        self.shidt_lower = self.min(self.responses_mean)

    def __call__(self, X):
        return norm.cdf(X, loc=self.mean, scale=self.std)

    def cdf(self, X):
        return self.cdf_function((self.mean, self.std), X)

    def shift_cdf(self, X):
        return self.shift_cdf_function((self.mean, self.sem), X, self.responses_mean)

    @staticmethod
    def static_nonlinearity(linearprediction, numepochs, response, prepoints, datapoints, tailpoints, numbins):
        """ turn linear prediction and responses into row vectors (so can bin using find) """

        linearpredictionrow = linearprediction.reshape(
            1, linearprediction.shape[1] * numepochs)

        responserow = response[:, prepoints+1:datapoints-(tailpoints+1)].reshape(
            1, len(np.range(prepoints+1, datapoints-(tailpoints+1))))*numepochs

        stepsize = 100/numbins
        binlimits = np.percentile(linearpredictionrow, np.arange(
            0, 100, stepsize), interpolate="midpoint")

        numbinlimits = len(binlimits)-1

        responses_mean = np.zeros(1, numbinlimits)
        responses_sem = np.zeros(1, numbinlimits)
        linpred_mean = np.zeros(1, numbinlimits)
        linpred_sem = np.zeros(1, numbinlimits)

        for ii in range(1, numbinlimits):
            indices = (
                linearprediction > binlimits(ii)
                & linearprediction <= binlimits(ii+1))

            responses_mean[ii] = np.mean(responserow(indices))
            responses_sem[ii] = np.std(
                responserow(indices))/np.sqrt(len(indices))
            linpred_mean[ii] = np.mean(linearpredictionrow(indices))
            linpred_sem[ii] = np.std(
                linearpredictionrow(indices))/np.sqrt(len(indices))

        return linpred_mean, linpred_sem, responses_mean, responses_sem

    def fit_nonlinearity(self, binned_linpred_mean, binned_responses_mean):
        """fit non-linearity"""
        # not used anymore?
        # fit a 5-degree polynomial
        # nonlinearmodel = np.polyfit(
        #    binned_linpred_mean.t, binned_responses_mean.T, deg=5)

        # fit a cummulative distribution function of a normal distribution
        # Norm Residual Cost Function
        def nrcf(z):
            return (
                norm.ppf(
                    binned_responses_mean
                    - self.shift_cdf_function(
                        z, binned_linpred_mean, binned_responses_mean)))

        # estimate parameters
        coeff = fmin(
            nrcf,
            x0=[np.mean(binned_linpred_mean), np.std(binned_linpred_mean)])

        mean, sem = coeff.x
        return mean, sem

    @staticmethod
    def cdf_function(z, X):
        return norm.cdf(X, z[1], z[2])

    @staticmethod
    def shift_cdf_function(z, X, Y):
        return ((norm.cdf(X, z[1], z[2]) * (max(Y)-min(Y))) + min(Y))
