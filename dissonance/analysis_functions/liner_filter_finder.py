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
    signal = np.atleast_2d(signal)
    response = np.atleast_2d(response)

    filterfft = (
        np.mean(fft(response) * np.conj(fft(signal)), axis=0)
        / np.mean(fft(signal) * np.conj(fft(signal)), axis=0))

    # NOTE adjust the freq cutoff for the length
    freqcutoff_adjusted = int(
        freqcutoff
        / (samplerate/len(signal)))  

	
    #filterfft[freqcutoff_adjusted:len(signal)-freqcutoff_adjusted] = 0.0

    linearfilter = np.real(ifft(filterfft))

    return linearfilter
