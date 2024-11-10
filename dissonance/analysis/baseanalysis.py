from abc import ABC, abstractmethod, abstractproperty
from typing import List, Optional

import pandas as pd

from ..epochtypes import EpochBlock, IEpoch
from .charting import MplCanvas


class IAnalysis(ABC):

    @property
    @abstractmethod
    def name(self): ...

    @property
    @abstractmethod
    def labels(self) -> List[str]: ...

    @property
    @abstractmethod
    def tracetype(self) -> IEpoch: ...

    @property
    @abstractmethod
    def tracestype(self) -> EpochBlock: ...

    @abstractmethod
    def plot(self, eframe: pd.DataFrame, canvas: Optional[MplCanvas] = None): ...
