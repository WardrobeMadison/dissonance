import matplotlib.pyplot as plt
import numpy as np


def calculate_psth(epoch, inc=50, outputfile=None, samplerate = 10000) -> np.ndarray:
    """Bin and count number of spikes. Subtract baseline firing rate from final psth."""
    # WHERE INC = (BIN SIZE IN MS) *10
    if hasattr(epoch, "traces"):
        x = np.zeros(epoch.traces.shape)
    else:
        x = np.zeros(epoch.trace.shape)

    x[epoch.spikes] = 1
    psth = np.fromiter([np.sum(x[ii : ii + inc]) for ii in range(0, epoch.trace.shape[0], inc)], dtype=float)

    # adjust for baseline
    psth = (samplerate/inc) * (psth - np.mean(psth[: int(epoch.pretime // inc)]))

    return psth
