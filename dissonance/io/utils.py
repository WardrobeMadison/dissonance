import pandas as pd
from .. import analysis, viewer

def open_browsing_window(epochio, filterpath):
    try:
        lsa = analysis.BrowsingAnalysis()
        startdates_to_exclude = set(pd.read_csv(filterpath, parse_dates=["startdate"]).iloc[:, 0].values)
        viewer.run(epochio, lsa, startdates_to_exclude, filterpath)
    except SystemExit:
        ...
    except Exception as e:
        print(e)
    finally:
        assert True