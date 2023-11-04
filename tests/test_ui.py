import pytest
from pathlib import Path
import pandas as pd
from dataclasses import dataclass

from dissonance import analysis, init_log, io, viewer
from .constants import MAP_DIR

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
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/saccade/GG2_saccade.txt"),
    protocols=["SaccadeTrajectory2"],
    paramnames=["led", "protocolname", "celltype",
                "genotype", "cellname", "lightmean", "startdate"],
    splits=["genotype","lightmean", "celltype", "cellname"],
)

AdaptingSteps = Params(
    name="AdaptingSteps",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/adaptingsteps/adapting_steps_5000.txt"),
    #filter_path=Path(
    #"/home/joe/Projects/analysis/filters/adaptingsteps/adapting_steps_8000.txt"),
    protocols=["AdaptingSteps"],
    paramnames=["led", "protocolname", "celltype",
                "genotype", "step_magnitude", "cellname", "startdate","variable_flash_time"],
    splits=["genotype", "celltype", "step_magnitude", "cellname","variable_flash_time"]
)

ContrastResponse = Params(
    name="ContrastResponse",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/contrastresponse/GG2_5000_CRF.txt"),
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

LedPulseOFFTRodSpikes = Params(
    name="LedPulseOFFTRodSpikes",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/GG2OFFTledpulsespikes/GG2OFFTledpulsespikes.txt"),
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

GA1Spikes = Params(
    name="GA1Spikes",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/GA1ledpulsespikes/temp_from_other.txt"),
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

GA1SpikesFamily = Params(
    name="GA1SpikesFamily",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/GA1ledpulsefamilyspikes/GA1LedPulseFamilySpikes.txt"),
    protocols=["LedPulseFamily"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["led","holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

GA1Excitation = Params(
    name="GA1Excitation",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/GA1ledpulseexcitation/GA1_bothLED_nobadepochsUNFINISHED.txt"), #rod and cone
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

LedPulseOFFSRodSpikes = Params(
    name="LedPulseOFFSRodSpikes",
    filter_path=Path(
        #"/home/joe/Projects/analysis/filters/GG2OFFSledpulsespikes/GG2OFFSledpulsespikes.txt"),
        "/home/joe/Projects/analysis/filters/GG2OFFSledpulsespikes/filtered_for_pretty_avg_PSTHs_GG2OFFSledpulsespikes.txt"),
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)

Inhibition = Params(
    name="Inhibition",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/GG2OFFTledpulseinhibition/arvo.txt"),
    protocols=["LedPulse"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "genotype", "lightmean",
            "celltype", "cellname", "lightamplitude"],
)
PairedPulse = Params(
    name="PairedPulse",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/ledpairedpulse/1000r*LedPairPulseFilters.txt"),
    protocols=["LedPairedPulseFamily", "LedPairedPulseFamilyOriginal"],
    paramnames=["led", "celltype", "genotype", "cellname", "tracetype", "backgroundval",
                "lightamplitude", "lightmean", "protocolname", "intime2", "startdate", "holdingpotential"],
    splits=["genotype", "celltype", "cellname", "intime2"],
)

ExpandingSpots = Params(
    name="ExpandingSpots",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/expandingspots/expandingspots.txt"),
    protocols=["ExpandingSpots"],
    paramnames=["protocolname", "celltype", "cellname", "genotype", "startdate",
                "tracetype", "current_spot_size", "background_intensity", "spot_intensity"],
    splits=["genotype", "celltype", "cellname",
            "background_intensity", "spot_intensity","current_spot_size"],
)

Weber = Params(
    name="Weber",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/weber/gg2_Weber.txt"),
    protocols=["LedPulseFamily"],
    paramnames=["led", "protocolname", "celltype", "genotype", "cellname",
                "lightmean", "lightamplitude", "tracetype", "startdate", "holdingpotential"],
    splits=["holdingpotential", "celltype", "genotype", "lightmean", "lightamplitude", "cellname",],
)

SineWavePulse = Params(
    name="SineWavePulse",
    filter_path=Path(
        "/home/joe/Projects/analysis/filters/ledpairedpulse/1000r*LedPairPulseFilters.txt"),
    protocols=["LedPairedSineWavePulse"],
    paramnames=["led", "celltype", "genotype", "cellname", "tracetype", "backgroundval",
                "lightamplitude", "lightmean", "protocolname", "first_wave_contrast","second_wave_contrast",
                "first_wave_frequency", "second_wave_frequency", "second_wave_time", "first_wave_time", "startdate", "holdingpotential"],
    splits=["genotype", "celltype", "cellname", "first_wave_contrast","second_wave_contrast"],
)


parameters = [
    (["GG2 KO", "GG2 control"], Saccade),
    (["GG2 KO", "GG2 control"], ContrastResponse),
    (["GA1 KO", "GG2 control", "GG2 KO","GA1 control"], ExpandingSpots),
    (["GG2 KO", "GG2 control"], LedPulseOFFSRodSpikes),
    (["GG2 KO", "GG2 control"], AdaptingSteps),
    (["GA1 KO", "GA1 control"], GA1Spikes),
    (["GA1 KO", "GA1 control"], GA1Excitation),
    (["GG2 KO", "GG2 control"], PairedPulse),
    (["GG2 KO", "GG2 control"], Weber),
    (["GG2 KO", "GG2 control"], SineWavePulse),
    (["GA1 KO", "GA1 control"], GA1SpikesFamily),
]


@pytest.mark.parametrize("folders,gui_params", parameters, ids=[f"{p.name}: {(', '.join(f))}" for f, p in parameters])
def test_window_browsing(folders, gui_params):
    try:
        paramnames, protocols, filter_path, splits = (
            gui_params.paramnames,
            gui_params.protocols,
            gui_params.filter_path,
            gui_params.splits
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


def get_parameters(paramnames, paths):
    dr = io.DissonanceReader(paths)

    params = dr.to_params(paramnames)
    return params


def get_paths(folders):
    paths = []
    for fldr in folders:
        paths.extend(
            [
                file
                for ii, file in enumerate((MAP_DIR/fldr).glob("*.h5"))
            ]
        )
    return paths
