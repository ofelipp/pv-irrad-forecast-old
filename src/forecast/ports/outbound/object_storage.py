# ! ./venv/bin/python3.10

from abc import ABCMeta, abstractmethod

from src.domain.data import Data


class ObjectStorage:
    __metadata__ = ABCMeta

    @abstractmethod
    def put_object(self, data: Data):
        raise NotImplementedError()
