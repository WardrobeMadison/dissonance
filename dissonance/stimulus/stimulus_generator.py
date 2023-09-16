from abc import abstractmethod

class StimulusGenerator:

    @abstractmethod
    def from_epoch(self):
        ...

    @property
    @abstractmethod
    def protocol(self):
        ...

    @abstractmethod
    def generate(self):
        ...