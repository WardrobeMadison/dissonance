import multiprocessing as mp

from dissonance.io import SymphonyIO
from tests.test_add_info import zip_raw_map_directories


def rename_all_in_folder(folder):
    print(folder)
    for rawfile, mapfile in zip_raw_map_directories(folder):
        print(f"\t{mapfile.name}")
        rdr = SymphonyIO(rawfile)
        rdr.update_epoch_name(mapfile)


def main():
    folders = ["GG2 control", "GG2 KO", "GA1 control", "GA1 KO"]  # "WT", "DR",

    with mp.Pool(len(folders)) as p:
        for _ in p.map(rename_all_in_folder, folders):
            ...


if __name__ == "__main__":
    main()
