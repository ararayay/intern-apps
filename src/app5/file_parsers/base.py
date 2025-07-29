from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def parse(self):
        pass
