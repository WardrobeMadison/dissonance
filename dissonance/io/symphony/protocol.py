import re

import h5py

from dissonance.io.symphony.epoch import Epoch
from dissonance.io.symphony.utils import convert_if_bytes


class Protocol:

    re_name = re.compile(r".*edu\.wisc\.sinhalab\.protocols\.([\w\d ]+)-.*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        # HACK MEANT TO REMOVE ORIGINAL FROM LEDPAIREDPULSEFAMILYORIGINAL
        self.name = self.re_name.match(group.name)[1].replace("Original", "")

    def __str__(self):
        return f"EpochBlock({self.name})"

    def __iter__(self):
        for key, val in self.group["protocolParameters"].attrs.items():
            yield key, convert_if_bytes(val)

    def __getitem__(self, value):
        val = self.group["protocolParameters"].attrs[value]
        return convert_if_bytes(val)

    def get(self, value, default=None):
        val = self.group["protocolParameters"].attrs.get(value, default)
        return convert_if_bytes(val)

    @property
    def children(self):
        for name in self.group["epochs"]:
            yield Epoch(self.group[f"epochs/{name}"])
