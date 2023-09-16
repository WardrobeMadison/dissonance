import itertools
from collections import defaultdict

import pandas as pd
import numpy as np

from . import baseepoch as bt 
from . import spikeepoch as st
from . import wholeepoch as wt
from . import sacaadeepoch as sa
from . import chirpepoch as ce
from . import adaptingsteps as ae
from . import expandingspots as es

def groupby(frame:pd.DataFrame, grpkeys) -> pd.DataFrame:
	"""
	Convert Traces to table with Epochs grouped by grpkeys
	"""
	defaultdict(list)
	epochtype =  type(frame.epoch.iloc[0])# ASSUME SINGLE TYPE PER LIST

	# TODO make this dynamic within epoch factory
	if epochtype == wt.WholeEpoch: types = wt.WholeEpochs
	elif epochtype == st.SpikeEpoch: types = st.SpikeEpochs
	elif epochtype == sa.SaccadeEpoch: types = sa.SaccadeEpochs
	elif epochtype == ce.ChirpEpoch: types = ce.ChirpEpochs
	elif epochtype == ae.AdaptingStepsEpoch: types = ae.AdpatingStepsEpochs
	elif epochtype == es.ExpandingSpotsEpoch: types = es.ExpandingsSpotsEpochs
	else: types = None

	data = []
	for key, grp in frame.groupby(grpkeys):
		data.append([*key, types(grp["epoch"].values)])

	
	return pd.DataFrame(columns = [*grpkeys, "epoch"], data=data)

def filter(epochs, **kwargs):
	out = []
	for epoch in epochs:
		condition = all([
			getattr(epoch, key) == val
			for key, val in kwargs.items()
		])
		if condition: out.append(epoch)
	tracetype = type(epochs)
	return tracetype(out)




