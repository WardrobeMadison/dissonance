import numpy as np
from scipy.fftpack import fft, ifft


def linear_filter_finder(signal, response, samplerate, freqcutoff):
    """this function will find the linear filter that changes row vector "signal" 
    into a set of "responses" in rows.  "samplerate" and "freqcuttoff" 
    (which should be the highest frequency in the signal) should be in HZ.
    The linear filter is a cc normalized by the power spectrum of the signal

    FiterFft computation with dividing by power spectrum gives vertical plot 
    for non-linearity, though the linearFilter plot isn't that different;
    also the predicted response is almost a flat line w.r.t measure response.
    """

    filterfft = (
        np.mean((fft(response, None, 2) * np.conj(fft(signal, None, 2))), 1)
        / np.mean(fft(signal, None, 2) * np.conj(fft(signal, None, 2)), 1))

    # NOTE adjust the freq cutoff for the length
    freqcutoff_adjusted = np.floor(
        freqcutoff
        / (samplerate/len(signal)))  

    filterfft[:, 1+freqcutoff_adjusted:len(signal)-freqcutoff_adjusted] = 0

    linearfilter = np.real(ifft(filterfft))

    return linearfilter
