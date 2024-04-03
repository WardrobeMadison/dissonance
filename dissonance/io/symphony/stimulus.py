import re
from typing import Iterator

import h5py

from dissonance.io.symphony.utils import convert_if_bytes


class Stimulus:

    re_name = re.compile(r"^([a-zA-Z0-9_ ]*)-.*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        self.name = self.re_name.match(self.group.name.split("/")[-1])[1]

        self._parameters = self.group["parameters"].attrs

    @property
    def parameters(self):
        return self._parameters

    def __getitem__(self, value):
        return self._parameters[value]

    def __iter__(self) -> Iterator[dict[str, object]]:
        for key, val in self.group["parameters"].attrs.items():
            yield key, convert_if_bytes(val)
