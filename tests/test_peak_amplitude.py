# 20240426B_Cell1
from pathlib import Path
import dissonance
from dissonance.epochtypes.ns_epochtypes import groupby


def test_peak_amplitude():
    lightmean = 1000
    lightamp = 1000

    protocol = "LedPulseFamily"
    filterfilepath = Path("filters/weber/gg2_Weber.txt")
    paramnames = ["led", "protocolname", "celltype", "genotype", "cellname",
                "tracetype", "backgroundval", "lightamplitude", "lightmean", "startdate"]

    path = Path(r"C:\Users\nagyj\Projects\datastore\dissonance\GG2 control\2024-04-26B.h5")
    filters = {"protocolname": protocol},

    dr = dissonance.io.DissonanceReader([path])

    ef = dr.to_epoch_table(paramnames, filterpath=filterfilepath, filters=filters, nprocesses=1,)
    ef["genotype"] = ef.genotype.str.replace("control", "Control")

    df = ef.loc[
        (ef.tracetype == "spiketrace") 
        & (ef.celltype == "RGC\ON-alpha")
        & (ef.led == "UV LED")]

    df.backgroundval.unique()

    df = groupby(df, 
                ["genotype", "cellname", "lightmean", "lightamplitude"])

