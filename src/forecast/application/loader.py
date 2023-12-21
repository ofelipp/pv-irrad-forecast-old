# ! ./venv/bin/python3.10

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pathlib import Path
import pickle

from src.domain.model import Model


MODELS_PATH = "model/schema/"


class LoaderModelsInterface(ABC):
    """Load models for service forecast"""

    @abstractmethod
    def load_models(self, path: str) -> dict:
        raise NotImplementedError()


class HourLoaderModels(LoaderModelsInterface):
    """Load models for an hour for service forecast"""

    def load_models(self, path: str) -> dict[str:Model]:
        # TODO: implement th load method
        return {
            model.stem: f"loading {model.stem}" for model in self.__search_models(path)
        }

    def __search_models(self, path: str) -> list:
        return list(Path(path).glob("*.pickle"))


@dataclass
class StationLoaderModels(LoaderModelsInterface):
    """Load models for a station (including all hours) for service forecast"""

    def load_models(self, path: str) -> dict:
        return {
            model.stem: f"loading {model.stem}" for model in self.__search_models(path)
        }
        # for hour_path in self.__search_avaiable_hours(path):
        #     self.models[hour_path.name] = self.loader.load_models(hour_path)

    def __search_models(self, path: str) -> list:
        return list(Path(path).rglob("*.pickle"))
        # [directory for directory in Path(path).iterdir() if directory.is_dir()]
