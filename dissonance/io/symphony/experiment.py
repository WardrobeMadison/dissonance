import re

import h5py

from dissonance.io.symphony.cell import Cell
from dissonance.io.symphony.groupbase import GroupBase


class Experiment(GroupBase):

    re_name = re.compile(r"experiment-.*")

    def __init__(self, parent: h5py.Group):
        super().__init__(parent)

    def name(self):
        return self._name

    @property
    def children(self):
        for name in self.group["epochGroups"]:
            yield Cell(self.group[f"epochGroups/{name}"])
