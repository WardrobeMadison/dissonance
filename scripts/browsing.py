import sys

sys.path.append("../")

from dataclasses import dataclass
from pathlib import Path

import click
import pandas as pd

from dissonance import analysis, init_log, io, viewer

ROOT_DIR = Path.home() / "Projects/datastore"
MAPPED_DIR = Path.home() / "Projects/datastore/dissonance"
RAW_DIR = Path.home() / "Projects/datastore/sinhalab/experiments"


logger = init_log()


@dataclass
class Params:
    name: str
    filter_path: Path
    protocols: str
    paramnames: list[str]
    splits: list[str]


Saccade = Params(
    name="Saccade",
    filter_path=Path("~/Projects/analysis/filters/saccade/GG2_saccade.txt"),
    protocols=["SaccadeTrajectory2"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname", "lightmean", "startdate"],
    splits=["genotype", "lightmean", "celltype", "cellname"],
)

AdaptingSteps = Params(
    name="AdaptingSteps",
    filter_path=Path("~/Projects/analysis/filters/adaptingsteps/adapting_steps_spikes_accounted.txt"),
    protocols=["AdaptingSteps"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "startdate",
        "variable_flash_time",
    ],
    splits=["genotype", "celltype", "cellname", "variable_flash_time"],
)

ContrastResponse = Params(
    name="ContrastResponse",
    filter_path=Path("~/Projects/analysis/filters/contrastresponse/GG2_5000_CRF.txt"),
    protocols=["LedPulse"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "lightmean",
        "lightamplitude",
        "tracetype",
        "startdate",
        "holdingpotential",
    ],
    splits=["holdingpotential", "genotype", "lightmean", "celltype", "cellname", "lightamplitude"],
)

LedPulseOFFTRodSpikes = Params(
    name="LedPulseOFFTRodSpikes",
    filter_path=Path("~/Projects/analysis/filters/GG2OFFTledpulsespikes/GG2OFFTledpulsespikes.txt"),
    protocols=["LedPulse"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "lightmean",
        "lightamplitude",
        "tracetype",
        "startdate",
        "holdingpotential",
    ],
    splits=["holdingpotential", "genotype", "lightmean", "celltype", "cellname", "lightamplitude"],
)

GA1Spikes = Params(
    name="GA1Spikes",
    filter_path=Path("~/Projects/analysis/filters/GA1ledpulsespikes/temp_from_other.txt"),
    protocols=["LedPulse"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "lightmean",
        "lightamplitude",
        "tracetype",
        "startdate",
        "holdingpotential",
    ],
    splits=["holdingpotential", "genotype", "lightmean", "celltype", "cellname", "lightamplitude"],
)

LedPulseOFFSRodSpikes = Params(
    name="LedPulseOFFSRodSpikes",
    filter_path=Path(
        # "~/Projects/analysis/filters/GG2OFFSledpulsespikes/GG2OFFSledpulsespikes.txt"),
        "~/Projects/analysis/filters/GG2OFFSledpulsespikes/filtered_for_pretty_avg_PSTHs_GG2OFFSledpulsespikes.txt"
    ),
    protocols=["LedPulse"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "lightmean",
        "lightamplitude",
        "tracetype",
        "startdate",
        "holdingpotential",
    ],
    splits=["holdingpotential", "genotype", "lightmean", "celltype", "cellname", "lightamplitude"],
)

Inhibition = Params(
    name="Inhibition",
    filter_path=Path("~/Projects/analysis/filters/GG2OFFTledpulseinhibition/arvo.txt"),
    protocols=["LedPulse"],
    paramnames=[
        "led",
        "protocolname",
        "celltype",
        "genotype",
        "cellname",
        "lightmean",
        "lightamplitude",
        "tracetype",
        "startdate",
        "holdingpotential",
    ],
    splits=["holdingpotential", "genotype", "lightmean", "celltype", "cellname", "lightamplitude"],
)

ExpandingSpots = Params(
    name="ExpandingSpots",
    filter_path=Path("~/Projects/analysis/filters/expandingspots/expandingspots.txt"),
    protocols=["ExpandingSpots"],
    paramnames=[
        "protocolname",
        "celltype",
        "cellname",
        "genotype",
        "startdate",
        "tracetype",
        "current_spot_size",
        "background_intensity",
        "spot_intensity",
    ],
    splits=[
        "genotype",
        "celltype",
        "cellname",
        "background_intensity",
        "spot_intensity",
        "current_spot_size",
    ],
)

PairedPulse = Params(
    name="PairedPulse",
    filter_path=Path("~/Projects/analysis/filters/ledpairedpulse/1000rstarLedPairPulseFilters.txt"),
    protocols=["LedPairedPulseFamily", "LedPairedPulseFamilyOriginal"],
    paramnames=[
        "led",
        "celltype",
        "genotype",
        "cellname",
        "tracetype",
        "backgroundval",
        "lightamplitude",
        "lightmean",
        "protocolname",
        "intime2",
        "startdate",
        "holdingpotential",
    ],
    splits=["genotype", "celltype", "cellname", "intime2"],
)

parameters = dict(
    Saccade=(["GG2 KO", "GG2 control"], Saccade),
    ContrastResponse=(["GG2 KO", "GG2 control"], ContrastResponse),
    ExpandingSpots=(["GA1 KO", "GG2 control", "GG2 KO", "GA1 control"], ExpandingSpots),
    LedPulseOFFSRodSpikes=(["GG2 KO", "GG2 control"], LedPulseOFFSRodSpikes),
    AdaptingSteps=(["GG2 KO", "GG2 control"], AdaptingSteps),
    GA1Spikes=(["GA1 KO", "GA1 control"], GA1Spikes),
)


def test_window_browsing(folders, gui_params):
    try:
        paramnames, protocols, filter_path, splits = (
            gui_params.paramnames,
            gui_params.protocols,
            gui_params.filter_path,
            gui_params.splits,
        )

        # read data into epoch io object
        dr = io.DissonanceReader.from_folders(folders)
        epochio = dr.to_epoch_io(paramnames, None, filter_path, protocols)

        lsa = analysis.BrowsingAnalysis(splits)
        viewer.run(epochio, lsa, epochio.unchecked, filter_path)

    except SystemExit as e:
        ...
    finally:
        assert True


@click.group()
def cli(): ...


@cli.command()
@click.argument("paramname", type=click.STRING)
def browse(paramname: str):
    folders, gui_params = parameters["paramname"]
    test_window_browsing(folders, gui_params)


if __name__ == "__main__":
    cli()
