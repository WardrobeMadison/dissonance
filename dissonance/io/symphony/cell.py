import re
from pathlib import Path

import h5py

from dissonance.io.symphony.protocol import Protocol
from dissonance.io.symphony.utils import convert_if_bytes


class Cell:

    RE_DATE = re.compile(r"^.*(\d{4}-?\d{2}-?\d{2})(\w\d?).*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        self.name = "epochGroup"

    def __str__(self):
        return str(self.group)

    @property
    def cellname(self):
        val = convert_if_bytes(self.group["source"].attrs["label"])
        if isinstance(val, str):
            return val
        else:
            return "MissingCellName"

    @property
    def celltype(self):
        val = convert_if_bytes(self.group["source/properties"].attrs["type"])
        if isinstance(val, str):
            return val
        else:
            return "MissingCellType"

    @property
    def cellkey(self):
        filepath = Path(self.group.file.filename)

        name = filepath.stem
        matches = self.RE_DATE.match(name)
        prefix = matches[1].replace("-", "") + matches[2]

        return f"{prefix}_{self.cellname}"

    @property
    def children(self):
        for name in self.group["epochBlocks"]:
            yield Protocol(self.group[f"epochBlocks/{name}"])
