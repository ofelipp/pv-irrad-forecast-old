# ! ./venv/bin/python3.10

from dataclasses import dataclass, field
from typing import Type

from src.domain.data import Data
from src.domain.model import Model

from src.forecast.ports.inbound.forecast_use_case import ForecastUseCase
from src.forecast.application import loader


@dataclass
class ForecastService(ForecastUseCase):
    loader: loader.StationLoaderModels
    models: dict[str : dict[str:Model]] = field(default_factory=dict)

    def load_models(self, path: str) -> list:
        self.models = loader.StationLoaderModels.load_models(path)

    def predict(self, X: Data) -> Data:
        return Data(data=[0, 0, 0])
