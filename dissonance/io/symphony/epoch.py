import datetime
import re

import h5py

from dissonance.io.symphony.background import Background
from dissonance.io.symphony.response import Response
from dissonance.io.symphony.stimulus import Stimulus


class Epoch:

    re_responses = re.compile(r"^([\w\d ]+)-.*$")
    re_protocolname = re.compile(r".*edu\.wisc\.sinhalab\.protocols\.([\w\d ]+)-.*$")

    def __init__(self, group: h5py.Group):
        self.group = group
        self.h5name = group.name
        self.name = "epoch"
        self.protocolname = self.re_protocolname.match(self.group.parent.parent.name)[1]

        self._backgrounds = dict()
        for name in self.group["backgrounds"]:
            background = Background(self.group[f"backgrounds/{name}"])
            self._backgrounds[background.name] = background

    def __str__(self):
        return f"Epoch({self.startdate})"

    @property
    def tracetype(self):
        if self.protocolname in ("ExpandingSpots",):
            return "spiketrace"
        elif "Amp1" in self._backgrounds.keys():
            val = self._backgrounds["Amp1"]["value"]
            if float(val) == 0.0:
                return "spiketrace"
            else:
                return "wholetrace"
        else:
            return "wholetrace"

    @property
    def holdingpotential(self):
        if "Amp1" in self._backgrounds.keys():
            val = self._backgrounds["Amp1"]["value"]
            if self.tracetype == "spiketrace":
                return "nan"
            elif val < 0:
                return "excitation"
            else:
                return "inhibition"
        else:
            return "nan"

    @property
    def backgrounds(self):
        return self._backgrounds

    @property
    def responses(self):
        for name in self.group["responses"]:
            yield Response(self.group[f"responses/{name}"])

    @property
    def startdate(self):
        dotNetTime = self.group.attrs["startTimeDotNetDateTimeOffsetTicks"]
        return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=int(dotNetTime // 10))

    @property
    def enddate(self):
        dotNetTime = self.group.attrs["endTimeDotNetDateTimeOffsetTicks"]
        return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=int(dotNetTime // 10))

    @property
    def stimuli(self):
        for name in self.group["stimuli"]:
            yield Stimulus(self.group[f"stimuli/{name}"])

    def protocol_parameters(self, key):
        return self.group["protocolParameters"].attrs.get(key, "None")
