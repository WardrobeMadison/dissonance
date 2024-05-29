import matplotlib.pyplot as plt
import numpy as np


def calculate_psth(epoch, inc=100, outputfile=None) -> np.ndarray:
    """Bin and count number of spikes. Subtract baseline firing rate from final psth."""
    # inc = 100 # 10 ms
    if hasattr(epoch, "traces"):
        x = np.zeros(epoch.traces.shape)
    else:
        x = np.zeros(epoch.trace.shape)

    x[epoch.spikes] = 1
    psth = np.fromiter([np.sum(x[ii : ii + inc]) for ii in range(0, epoch.trace.shape[0], inc)], dtype=float)

    # adjust for baseline
    psth = 100 * (psth - np.mean(psth[: int(epoch.pretime // 100)]))

    return psth
