from abc import ABC, abstractmethod
import numpy as np

class BaseAnomalyModel(ABC):

    @abstractmethod
    def fit(self, X: np.ndarray):
        pass

    @abstractmethod
    def score(self, X: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass
