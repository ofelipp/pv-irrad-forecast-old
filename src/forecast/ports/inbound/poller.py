# ! ./venv/bin/python3.10

from abc import ABCMeta, abstractmethod

from src.domain.data import Data


class Poller:
    __metadata__ = ABCMeta

    @abstractmethod
    def get_job(self) -> Data:
        raise NotImplementedError()
