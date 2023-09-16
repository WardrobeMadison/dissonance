import pandas as pd

from .trees import Node, Tree

class AnalysisTree(Tree):

    def __init__(self, name, splits, params: pd.DataFrame):
        self.name = name
        self.splits = splits
        self.plant(params)

    def plant(self, params: pd.DataFrame):
        self.labels = self.splits

        if "startdate" not in self.labels:
            self.labels = [*self.labels, "startdate"]
        
        # sorting params here will propogate to tree display.
        # much faster to use pandas API
        params = params.sort_values(self.labels)
        self.keys = params.loc[:, self.labels].values

        # CREATE TREE STRUCTURE
        super().__init__(self.name, self.labels, self.keys)
