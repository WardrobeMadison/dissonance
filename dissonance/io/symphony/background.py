import re
from typing import Dict, Iterator

import h5py

from dissonance.io.symphony.utils import convert_if_bytes


class Background:

    re_name = re.compile(r"^([\w\d @]+)-.*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        self.name = self.re_name.match(group.name.split("/")[-1])[1]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __getitem__(self, value):
        return convert_if_bytes(self.group.attrs[value])

    def __iter__(self) -> Iterator[Dict[str, object]]:
        for key, value in self.group.attrs.items():
            return key, convert_if_bytes(value)
