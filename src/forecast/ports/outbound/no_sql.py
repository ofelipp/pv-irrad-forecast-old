# ! ./venv/bin/python3.10

from abc import ABCMeta, abstractmethod

from src.domain.data import Data


class NoSQL:
    __metadata__ = ABCMeta

    @abstractmethod
    def insert(self, data: Data):
        raise NotImplementedError()
