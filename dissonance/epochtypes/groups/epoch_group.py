import numpy as np
import pandas as pd

from ...io.symphony.epoch import Epoch


class EpochGroup:

    def __init__(self, keys: dict[str, object], epochs: list[Epoch]):
        self.keys = keys
        self.epochs = epochs

    @property
    def trace(self) -> float:
        return np.mean(self.traces, axis=0)

    @property
    def to_df(self) -> pd.DataFrame: ...
