import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq
import plotly.express as px
import matplotlib.pyplot as plt

plt.style.use("seaborn")

def filter_spikes(signal, samplerate, cutoff_cycles_per_second, plt_process=False, x_bound=100):
    seconds = len(signal)/10000
    time = np.linspace(0, seconds, int(seconds*samplerate))

    W = fftfreq(signal.size, d=time[1]-time[0])
    f_signal = rfft(signal)

    px.scatter(signal)

    cut_f_signal = f_signal.copy()
    cut_f_signal[(W > cutoff_cycles_per_second)] = 0
    cut_signal = irfft(cut_f_signal)

    if plt_process:
        fig, axes = plt.subplots(2, 2, constrained_layout=True)

        axes[0, 0].plot(time, signal)

        axes[0, 1].plot(W, f_signal)
        axes[0, 1].set_xlim(0, x_bound)

        axes[1, 0].plot(W, cut_f_signal)
        axes[1, 0].set_xlim(0, 10)

        axes[1, 1].plot(signal, c='black', alpha=0.2, label="Original")
        axes[1, 1].plot(cut_signal, c='purple', alpha=0.8, label=f"Filterd w/ {cutoff_cycles_per_second} cycles/unit")
        axes[1,1].legend()

        fig.suptitle(f"Min from {signal.min():.0f} to {cut_signal.min():.0f}")
        fig.show()
    return cut_signal


signal = np.genfromtxt("~/Downloads/tojoe.txt")
cut_signal = filter_spikes(signal, 10000, 100, True)
