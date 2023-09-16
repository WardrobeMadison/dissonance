from .. import analysis, init_log, io, viewer


def open_browsing_analysis(epochio, splits, filter_path=None):
	if filter_path is not None:
		open(filter_path).read()
	lsa = analysis.BrowsingAnalysis(splits)
	viewer.run(epochio, lsa, filter_path)