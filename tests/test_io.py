import pytest
from functools import partial
import logging
from multiprocessing import Pool
from pathlib import Path

from dissonance import epochtypes, io, viewer, init_log
import dissonance.io.symphony.symphonyio
from .constants import ROOT_DIR, RAW_DIR, MAP_DIR

logger = init_log()

folders = [
    "GG2 KO",
    "GG2 control",
    "GA1 control",
    "GA1 KO"]


@pytest.mark.parametrize("folder", folders)
def test_all_to_h5(folder):
    rstarrdf = io.read_rstarr_table()

    wdir = RAW_DIR / folder

    wodir = (MAP_DIR / folder)
    wodir.mkdir(parents=True, exist_ok=True)

    files = [file for file in wdir.glob("*.h5")]
    func = partial(write_file, wodir=wodir, rstarrdf=rstarrdf, overwrite=False)

    with Pool(min(len(files), 6)) as p:
        for x in p.imap_unordered(func, files):
            print(x)


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

    rstarrdf = io.read_rstarr_table()
    write_file((RAW_DIR/geno) / filename,
               (MAP_DIR/geno), rstarrdf, overwrite=True)


def write_file(file, wodir, rstarrdf, overwrite=False):
    try:
        if (not overwrite) and ((wodir/file.name).exists()):
            return
        print(file)
        sr = dissonance.io.symphony.symphonyio.SymphonyIO(file, rstarrdf)
        sr.to_h5(wodir / file.name)
    except Exception as e:
        logger.warning(f"FILEFAILED {file}")
        logger.warning(e)

    return f"Done reading {file}"
