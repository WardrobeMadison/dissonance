import logging
from pathlib import Path

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class RStarrConverter:
    """Map symphony units to rstarr conversion. Detector is sensitive on each date, so table is maintained in data."""

    def __init__(self, valdate, path=None):
        self.valdate = valdate
        self.path = Path(__file__).parent.parent.parent.parent / \
            "data/rstarrmap.txt" if path is None else path
        self.df = self.read_rstarr_table(self.path)
        self.map = self.rstarr_map_to_dict(self.df, valdate)
        self.errors = set()

    @staticmethod
    def read_rstarr_table(path: Path) -> pd.DataFrame:
        rstarrdf = pd.read_csv(
            path,
            delimiter="\t",
            parse_dates=["startdate", "enddate"],
            dtype=dict(
                protocolname=str,
                led=str,
                lightamplitude=float,
                lightamplitude_rstarr=float,
                lightmean=float,
                lightmean_rstarr=float))
        return rstarrdf

    def get(self, protocolname, led, lightamp, lightmean) -> tuple[float, float]:
        """Get rstarr mapping. Adds to .errors and sets to -10000, -10000 if not found."""
        key = (protocolname, led, lightamp, lightmean)
        amp, mean = self.map.get(key, (None, None))

        if key is (None, None):
            set.add(
                ','.join(map(str, ((self.valdate, protocolname, led, lightamp, lightmean)))))
            amp, mean = -10000, -10000

        return amp, mean

    def rstarr_map_to_dict(self, df: pd.DataFrame, valdate) -> dict:
        """Convert rstarr table to dictionary based on valuation date"""
        dff = df.loc[
            (df.startdate <= valdate) & (df.enddate > valdate)
        ]

        if dff.shape[0] == 0:
            raise Exception(f"{valdate} is not in RStarr map")

        rstarrmap = dict()
        for _, row in dff.iterrows():
            rstarrmap[(row["protocolname"], row["led"], row["lightamplitude"], row["lightmean"])] = (
                row["lightamplitude_rstarr"], row["lightmean_rstarr"])
        return rstarrmap


S1 = np.dtype("|S1")


def convert_if_bytes(attr):
    if isinstance(attr, np.bytes_):
        return attr.decode()
    else:
        return attr
