import h5py


class GroupBase:

    re_name = ""

    def __init__(self, parent: h5py.Group):
        self.parent = parent
        for name in self.parent:
            if self.re_name.match(name):
                self._name = name

        self.group: h5py.Group = parent[name]

    @property
    def name(self) -> str:
        return self._name