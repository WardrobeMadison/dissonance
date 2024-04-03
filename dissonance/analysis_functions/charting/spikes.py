from pathlib import Path

import matplotlib.pyplot as plt

from ...epochtypes import SpikeEpoch
from ..spike_detection import TraceSpikeResult


def plt_psth(psth, nbins, outputfile: Path = None):
    plt.subplot()
    plt.grid(True)
    plt.plot(range(0, nbins), psth)
    plt.title("PSTH")
    plt.ylabel("Number of spikes / 10ms")
    plt.xlabel("Bin 10ms increments")
    if outputfile:
        plt.savefig(outputfile, dpi=150)
    plt.show()


def plt_spikes(epoch: SpikeEpoch, outputfile: Path = None):
    plt.subplot()
    plt.plot(epoch.trace)
    plt.grid(True)
    y = epoch.trace[epoch.spikes]
    plt.scatter(epoch.spikes, y, marker="x", c="#FFA500")

    plt.title(epoch.startdate)
    plt.ylabel("pA")
    plt.xlabel("10e-4 seconds")

    if outputfile:
        plt.savefig(outputfile, dpi=150)
    plt.show()
