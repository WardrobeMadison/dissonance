import sys

from multiprocessing import Pool

from dissonance.io.symphony.rstarr_converter import RStarrConverter
from dissonance.io.symphony.symphonyio import SymphonyIO

sys.path.append("..")
from pathlib import Path

import pytest

from dissonance import init_log, io
from dissonance.io import DissonanceUpdater

from .constants import MAP_DIR, RAW_DIR, ROOT_DIR

logger = init_log()

folders = ["GG2 control", "GG2 KO", "GA1 control", "GA1 KO"]  # "WT", "DR",


@pytest.mark.parametrize(
    "geno,filename",
    [
        ("GG2 KO", "2022-09-19B.h5"),
    ],
)
def test_update_rstarr_file(geno, filename):
    geno = "GG2 control"
    filename = "2023-12-29B.h5"

    rdr = SymphonyIO((RAW_DIR / geno) / filename)
    rdr.update_rstarr((MAP_DIR / geno) / filename)


@pytest.mark.parametrize("folder", folders)
def test_update_params_files(folder):
    """Update parameters within files"""
    if __debug__:
        for rawfile, mapfile in zip_raw_map_directories(folder):
            update(rawfile, mapfile)
    else:
        with Pool(8) as p:
            p.starmap(update, zip_raw_map_directories(folder))


def update(rawfile, mapfile):
    rdr = SymphonyIO(rawfile)
    rdr.update(mapfile, attrs=True)


@pytest.mark.parametrize("folder", folders)
def test_update_rstarr_files(folder):
    for rawfile, mapfile in zip_raw_map_directories(folder):
        try:
            rdr = SymphonyIO(rawfile)
            rdr.update_rstarr(mapfile)
        except Exception as e:
            logger.info(e)


@pytest.mark.parametrize("folder", folders)
def test_add_genotype_files(folder):
    """Add genotypes from folder name"""
    wdir = MAP_DIR / folder
    for file in wdir.glob("*.h5"):
        up = DissonanceUpdater(file)
        up.add_genotype(folder)


geno_filenames = [("GG2 KO", "2022-09-19B.h5")]


@pytest.mark.parametrize("geno,filename", geno_filenames)
def test_add_genotype_file(geno, filename):
    # CHANGE GENO TYPE (CORRESPONDS TO FOLDER) AND FILENAME
    genodir = MAP_DIR / geno
    up = DissonanceUpdater(genodir / filename)
    up.add_genotype(geno)


@pytest.mark.parametrize("folder", folders)
def test_update_cell_labels(folder):
    """Combine cellname and experiment date to make unique code"""
    wdir = MAP_DIR / folder
    for file in wdir.glob("*.h5"):
        up = DissonanceUpdater(file)
        up.update_cell_labels()


@pytest.mark.parametrize("folder", folders)
def test_update_spikes(folder):
    """Combine cellname and experiment date to make unique code"""
    wdir = MAP_DIR / folder
    for file in wdir.glob("*.h5"):
        up = DissonanceUpdater(file)
        up.update_spikes()


def zip_raw_map_directories(flder) -> list[tuple[Path, Path]]:
    filepaths = []

    rawfiles = [file for file in (RAW_DIR / flder).glob("*.h5")]
    rawstems = list(map(lambda x: x.stem, rawfiles))
    for file in (MAP_DIR / flder).glob("*.h5"):
        if file.stem in rawstems:
            filepaths.append([(RAW_DIR / flder) / file.name, (MAP_DIR / flder) / file.name])

    return filepaths
