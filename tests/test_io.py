import logging
from functools import partial
from pathlib import Path

import pytest
from multiprocess import Pool

import dissonance.io.symphony.symphonyio
from dissonance import epochtypes, init_log, io, viewer

from .constants import MAP_DIR, RAW_DIR, ROOT_DIR

logger = init_log()

folders = ["GG2 KO", "GG2 control", "GA1 control", "GA1 KO"]


@pytest.mark.parametrize("folder", folders)
def test_all_to_h5(folder):

    wdir = RAW_DIR / folder

    wodir = MAP_DIR / folder
    wodir.mkdir(parents=True, exist_ok=True)

    files = [file for file in wdir.glob("*.h5")]
    func = partial(write_file, wodir=wodir, overwrite=False)

    with Pool(min(len(files), 6)) as p:
        for x in p.imap_unordered(func, files):
            print(x)


@pytest.mark.parametrize("folder", folders)
def test_map_protocol(folder):
    protocolname = "LedPairedSineWavePulse"
    wdir = RAW_DIR / folder

    wodir = MAP_DIR / folder
    wodir.mkdir(parents=True, exist_ok=True)

    files = [file for file in wdir.glob("*.h5")]
    # func = partial(map_protocol, protocolname=protocolname, wodir=wodir)

    # with Pool(min(len(files), 6)) as p:
    #    for x in p.imap_unordered(func, files):
    #        print(x)

    for file in files:
        map_protocol(file, protocolname, wodir)


def get_missing_files():
    find_all_files = lambda dir: {
        (file.parent.name, file.name)
        for genodir in Path(dir).glob("*")
        for file in genodir.glob("*.h5")
        if file.parent.name != "DR"
    }
    src = find_all_files(RAW_DIR)
    dst = find_all_files(MAP_DIR)
    files = src - dst
    files = sorted(files)
    return files


files = get_missing_files()


@pytest.mark.parametrize("geno,filename", files, ids=(f"{x} {y}" for x, y in files))
def test_to_h5(geno, filename):
    write_file((RAW_DIR / geno) / filename, (MAP_DIR / geno), overwrite=True)


def map_protocol(file, protocolname, wodir):
    try:
        print(file)
        sr = dissonance.io.symphony.symphonyio.SymphonyIO(file)
        sr.map_protocol(protocolname, wodir / file.name)
    except Exception as e:
        logger.warning(f"FILEFAILED {file}")
        logger.warning(e)


def write_file(file, wodir, overwrite=False):
    try:
        if (not overwrite) and ((wodir / file.name).exists()):
            return
        print(file)
        sr = dissonance.io.symphony.symphonyio.SymphonyIO(file)
        sr.to_h5(wodir / file.name)
    except Exception as e:
        logger.warning(f"FILEFAILED {file}")
        logger.warning(e)

    return f"Done reading {file}"
