# ! ./venv/bin/python3.10

from abc import ABCMeta, abstractmethod

from src.domain.data import Data


class RelationalDatabase:
    __metadata__ = ABCMeta

    @abstractmethod
    def insert(self, data: Data):
        raise NotImplementedError()
