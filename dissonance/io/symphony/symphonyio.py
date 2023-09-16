import logging
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def read_rstarr_table():
    rstarrdf = pd.read_csv(
        Path(__file__).parent.parent.parent / "data/rstarrmap.txt",
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


def rstarr_map_to_dict(df: pd.DataFrame, valdate) -> Dict:
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




