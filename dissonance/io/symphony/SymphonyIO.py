from dissonance.analysis_functions import detect_spikes
from dissonance.io.symphony import symphonymapping as sm
from dissonance.io.symphony.cell import Cell
from dissonance.io.symphony.epoch import Epoch
from dissonance.io.symphony.experiment import Experiment
from dissonance.io.symphony.protocol import Protocol
from dissonance.io.symphony.utils import rstarr_map_to_dict


import h5py
import pandas as pd


import logging
import re
from pathlib import Path


class SymphonyIO:

    def __init__(self, path: Path, rstarrdf: pd.DataFrame):
        self.finpath = path
        self.fin = h5py.File(path)
        self.exp = Experiment(self.fin)
        self.fout = None

        # HACK assume genotype is name of parent folder
        self.genotype = path.parent.stem

        redate = re.compile(r"^(\d\d\d\d)-(\d\d)-(\d\d).*$")
        matches = redate.match(path.name)
        self.expdate = f"{matches[1]}-{matches[2]}-{matches[3]}"
        self.rstarmap = rstarr_map_to_dict(rstarrdf, self.expdate)

    def reader(self):
        for cell in self.exp.children:
            for protocol in cell.children:
                for epoch in protocol.children:
                    yield cell, protocol, epoch

    def to_h5(self, outputpath: Path):
        try:
            outputpath.parent.mkdir(parents=True, exist_ok=True)
            self.fout = h5py.File(outputpath, mode="w")
            expgrp = self.fout.create_group("experiment")
            for ii, (cell, protocol, epoch) in enumerate(self.reader()):

                epochgrp = expgrp.create_group(f"epoch{ii}")

                # ADD EPOCH ATTRIBUTES
                self._update_attrs(protocol, cell, epoch, epochgrp)

                # ADD RESPONSE DATA - CACHE SPIKES
                self._update_response(epoch, epochgrp)

                # ADD GROUP FOR EACH STIMULUS
                self._update_stimuli(epoch, epochgrp)

        except Exception as e:
            if self.fout is not None:
                self.fout.close()
            raise e
        finally:
            self.fout.close()

    def update(self, outputpath, attrs=False, responses=False, stimuli=False):
        try:
            self.fout = h5py.File(outputpath, mode="r+")
            expgrp = self.fout["experiment"]
            for ii, (cell, protocol, epoch) in enumerate(self.reader()):

                try:
                    epochgrp = expgrp[f"epoch{ii}"]

                    # ADD EPOCH ATTRIBUTES
                    if attrs:
                        self._update_attrs(protocol, cell, epoch, epochgrp)

                    # ADD RESPONSE DATA - CACHE SPIKES
                    if responses:
                        self._update_response(epoch, epochgrp)

                    # ADD GROUP FOR EACH STIMULUS
                    if stimuli:
                        self._update_stimuli(epoch, epochgrp)

                except KeyError:
                    epochgrp = expgrp.create_group(f"epoch{ii}")
                    self._update_attrs(protocol, cell, epoch, epochgrp)
                    self._update_response(epoch, epochgrp)
                    self._update_stimuli(epoch, epochgrp)

        except Exception as e:
            if self.fout is not None:
                self.fout.close()
            raise e

        self.fout.close()

    def update_rstarr(self, outputpath):
        try:
            self.fout = h5py.File(outputpath, mode="r+")
            expgrp = self.fout["experiment"]
            for ii, (cell, protocol, epoch) in enumerate(self.reader()):

                epochgrp = expgrp[f"epoch{ii}"]
                try:
                    del epochgrp.attrs["lightamplitude"]
                except KeyError:
                    ...
                try:
                    del epochgrp.attrs["lightmean"]
                except KeyError:
                    ...
                try:
                    del epochgrp.attrs["lightamplitudeSU"]
                except KeyError:
                    ...
                try:
                    del epochgrp.attrs["lightmeanSU"]
                except KeyError:
                    ...

                self._rstarr_conversion(protocol, epoch, epochgrp)

        except Exception as e:
            if self.fout is not None:
                self.fout.close()
            raise e

        self.fout.close()

    def _update_stimuli(self, epoch: Epoch, epochgrp: h5py.Group):
        # map to stimulus group
        stimuli_grp = epochgrp.create_group("stimuli")
        for stimuli in epoch.stimuli:
            stimds = stimuli_grp.create_group(stimuli.name)
            for key, val in stimuli:
                stimds.attrs[key.lower()] = val

    def _update_response(self, epoch: h5py.Group, epochgrp: h5py.Group):
        for response in epoch.responses:
            values = response.data
            ds = epochgrp.create_dataset(
                name=response.name, data=values, dtype=float)

            ds.attrs["path"] = response.h5name

            if (epoch.tracetype == "spiketrace") and (response.name == "Amp1"):
                spikes, violationidx = detect_spikes(values)

                if spikes is not None:
                    spds = epochgrp.create_dataset(
                        name="Spikes",
                        data=spikes,
                        dtype=float)

                if violationidx is not None:
                    spds.attrs["violation_idx"] = violationidx

    def _update_attrs(self, protocol: Protocol, cell: Cell, epoch: Epoch, epochgrp: h5py.Group):
        params = dict(
            path=epoch.h5name,
            cellname=cell.cellkey,
            celltype=cell.celltype,
            genotype=self.genotype,
            tracetype=epoch.tracetype,
            protocolname=protocol.name,
            startdate=str(epoch.startdate),
            enddate=str(epoch.enddate),
            interpulseinterval=protocol.get(
                "interpulseInterval", 0),
            led=protocol.get("led", 0),
        )

        self._rstarr_conversion(protocol, epoch, epochgrp)

        params["numberofaverages"] = protocol.get("numberOfAverages", 0.0)
        params["pretime"] = protocol.get("preTime", 0.0)

        # HACK need to separate parameter reads by protocol
        try:
            epochgrp.attrs["backgroundval"] = epoch.backgrounds["Amp1"]["value"]
        except:
            epochgrp.attrs["backgroundval"] = 0.0

        params.update(dict(
            stimtime=protocol.get("stimTime", 0.0),
            samplerate=protocol.get("sampleRate", 0.0),
            tailtime=protocol.get("tailTime", 0.0),
            ndf=epoch.protocol_parameters("ndf"),
            holdingpotential=epoch.holdingpotential,
        ))

        if protocol.name.lower() in ("ledpairedpulsefamily", "ledpairedpuslefamilyoriginal",):
            params.update(sm.PairedPulseFamilyParams(protocol, epoch).params)
        elif protocol.name.lower() == "chirpstimulusled":
            params.update(sm.ChirpStimulusLed(protocol).params)
        elif protocol.name == "ExpandingSpots":
            params.update(sm.ExpandingSpots(protocol, epoch).params)
        elif protocol.name == "AdaptingSteps":
            params.update(sm.AdapatingSteps(protocol, epoch).params)
        epochgrp.attrs.update(params)

    def _rstarr_conversion(self, protocol, epoch: Epoch, epochgrp):
        # HACK IF LEDPULSEFAMILY THEN LIGHTAMPLITUDE IS IN THE EPOCH FOLDER
        # TODO CHANGE READER TO FIND PARAMETERS BASED ON PROTOCOL
        # TODO CHANGE EPOCH CLASSES TO VARY BASED ON PROTOCOL, CELL, ETC...
        if protocol.name == "LedPulseFamily":
            lightamp = epoch.protocol_parameters("lightAmplitude")
        elif protocol == "ChirpStimulusLED":
            lightamp = 0.0
        elif protocol == "ExpandingSpots":
            lightamp = 0.0
        else:
            lightamp = protocol.get("lightAmplitude", None)
            if lightamp is None:
                lightamp = protocol.get("firstLightAmplitude", None)
            if lightamp is None:
                lightamp = 0.0
                logging.info(f"{str(epoch.startdate)}: no lightamplitude.")

        lightmean = protocol.get("lightMean", None)
        if protocol == "ChirpStimulusLED":
            lightmean = protocol["backgroundIntensity"]
        elif protocol == "ExpandingSpots":
            lightmean = protocol["backgroundIntensity"]
        elif lightmean is None:
            lightmean = 0.0
            logging.warning(f"{str(epoch.startdate)}: no lightmean.")

        epochgrp.attrs["lightamplitudeSU"] = lightamp
        epochgrp.attrs["lightmeanSU"] = lightmean

        try:
            epochgrp.attrs["lightamplitude"], epochgrp.attrs["lightmean"] = (
                self.rstarmap[
                    (protocol.name, protocol.get("led", None), lightamp, lightmean)])
        except KeyError:
            logging.warning(
                f"RStarrConversionError: {','.join(map(str, (self.expdate, protocol.name, protocol.get('led',None),lightamp, lightmean)))}")
            epochgrp.attrs["lightamplitude"], epochgrp.attrs["lightmean"] = -10000, -10000