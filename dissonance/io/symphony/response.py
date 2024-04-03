import re
from typing import Dict, Iterator

import h5py
import numpy as np

from dissonance.io.symphony.utils import convert_if_bytes


class Response:

    re_name = re.compile(r"^([\w\d ]+)-.*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        self.name = self.re_name.match(group.name.split("/")[-1])[1]

        self._parameters: Dict = {
            "samplerate": self.group.attrs["sampleRate"],
            "samplerateunits": self.group.attrs["sampleRateUnits"],
        }

    def __str__(self):
        return f"Response({self.name})"

    def __repr__(self):
        return f"Response({self.name})"

    @property
    def data(self):
        vals = np.array(self.group["data"][:], dtype=[("v", "<f8"), ("units", "<U16")])
        return vals["v"]

    @property
    def parameters(self) -> Dict:
        return self._parameters

    def __getitem__(self, value):
        return self._parameters[value]

    def __iter__(self) -> Iterator[Dict[str, object]]:
        for key, value in self._parameters:
            yield key, convert_if_bytes(value)

    def get(self, value, default):
        return self._parameters.get(value, default)
