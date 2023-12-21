# ! ./venv/bin/python3.10

from abc import ABCMeta, abstractmethod

from src.domain.data import Data


class ForecastUseCase:
    __metadata__ = ABCMeta

    @abstractmethod
    def predict(self, X: Data) -> Data:
        raise NotImplementedError()
