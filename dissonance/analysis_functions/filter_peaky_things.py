import numpy as np
import pandas as pd

"""Filter peaky things from whole cell spike trains using FBEWMA
"""


class PeakFilter:

    def __init__(self, trace: np.ndarray, delta: float = 0.10, clip_range: float = 3000, span: int = 10):

        self.trace = trace
        self.delta = delta
        self.clip_range = clip_range
        self.span = span

        self.trace_filtered = PeakFilter.filter_peaky_things(
            self.trace, self.delta, self.clip_range, self.span
        )

    @classmethod
    def from_h5(cls, epochgroup):
        """instantiate class from h5 group"""
        ...

    @property
    def params(self):
        return dict(delta=self.delta, clip_range=self.clip_range, span=self.span)

    @staticmethod
    def filter_peaky_things(
        trace: np.ndarray, delta: float = 0.10, clip_range: float = 3000, span: int = 10
    ) -> pd.DataFrame:
        """Filter peaky things from whole ceell spike trains using FBEWMA

        Parameters
        ----------
        trace : np.ndarray
            spike train
        delta : float, optional
            distance away from FBEWMA that data should be removed, by default 0.10
        clip_range : int, optional
            random value below this trigger a spike, by default -3000
        span : int, optional
            sample window of FBEWMA, by default 10

        Returns
        -------
        pd.DataFrame() :
            x, y_spikey, y_interpolated
        """

        high_clip, low_clip = (clip_range, -1 * clip_range)

        ef = pd.DataFrame()
        ef["y_spikey"] = trace
        ef["x"] = np.arange(len(trace)) + 1
        ef["y_clipped"] = PeakFilter.clip_data(ef["y_spikey"].tolist(), high_clip, low_clip)
        ef["y_ewma_fb"] = PeakFilter.ewma_fb(ef["y_clipped"], span)
        ef["y_remove_outliers"] = PeakFilter.remove_outliers(
            ef["y_clipped"].tolist(), ef["y_ewma_fb"].tolist(), delta
        )
        ef["y_interpolated"] = ef["y_remove_outliers"].interpolate()

        return ef[["x", "y_spikey", "y_interpolated"]].fillna(0.0)

    @staticmethod
    def clip_data(unclipped, high_clip, low_clip):
        """Clip unclipped between high_clip and low_clip.
        unclipped contains a single column of unclipped data."""

        # convert to np.array to access the np.where method
        np_unclipped = np.array(unclipped)
        # clip data above HIGH_CLIP or below LOW_CLIP
        cond_high_clip = (np_unclipped > high_clip) | (np_unclipped < low_clip)
        np_clipped = np.where(cond_high_clip, np.nan, np_unclipped)
        return np_clipped.tolist()

    @staticmethod
    def ewma_fb(df_column, span):
        """Apply forwards, backwards exponential weighted moving average (EWMA) to df_column."""
        # Forwards EWMA.
        fwd = pd.Series.ewm(df_column, span=span).mean()
        # Backwards EWMA.
        # TODO should this span be ten?
        bwd = pd.Series.ewm(df_column[::-1], span=span).mean()
        # Add and take the mean of the forwards and backwards EWMA.
        stacked_ewma = np.vstack((fwd, bwd[::-1]))
        fb_ewma = np.mean(stacked_ewma, axis=0)
        return fb_ewma

    @staticmethod
    def remove_outliers(spikey, fbewma, delta):
        """Remove data from df_spikey that is > delta from fbewma."""
        np_spikey = np.array(spikey)
        np_fbewma = np.array(fbewma)
        cond_delta = np.abs(np_spikey - np_fbewma) > delta
        np_remove_outliers = np.where(cond_delta, np.nan, np_spikey)
        return np_remove_outliers
