"""Rename existing protocol name
"""
from pathlib import Path
import h5py

def rename_protocol(rdir:Path, oldname:str, newname:str):
    print(f"Convert {oldname} to {newname}")
    for path in rdir.glob("*.h5"):
        print(path.stem)
        with h5py.File(path, "r+") as file:
            for epochname in file["experiment"]:
                epoch = file[f"experiment/{epochname}"]

                if epoch.attrs["protocolname"] == oldname:
                    print(f"Renaming epoch {epoch}.")
                    del epoch.attrs["protocolname"]
                    epoch.attrs["protocolname"] == newname
                    file.flush()

if __name__ == "__main__":
    rdir = Path(r"/home/joe/Projects/datastore/dissonance/GG2 control")
    rename_protocol(
        rdir,
        "LedPairedPulseFamilyOriginal",
        "LedPairedPulseFamily")