import pandas as pd
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ..analysis import IAnalysis
from ..analysis.charting import MplCanvas


class GraphWidget(MplCanvas):
    redrawCanvas = pyqtSignal()
    currentPlots = pyqtSignal(list)

    def __init__(self, parent, analysis: IAnalysis):
        super().__init__(parent)

        self.analysis = analysis
        self.currentplots = []

    @pyqtSlot(str, object)
    def plot(self, level: str, eframe: pd.DataFrame):
        try:
            self.analysis.plot(level, eframe, self)
            self.currentplots = self.analysis.currentplots

            self.draw()
            self.currentPlots.emit(self.currentplots)
        except Exception as e:
            print(e)
