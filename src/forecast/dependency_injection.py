# ! ./venv/bin/python3.10

from dataclasses import dataclass, field

from src.forecast.ports.inbound.poller import Poller
from src.forecast.ports.inbound.forecast_use_case import ForecastUseCase

from src.forecast.adapters.inbound.sqs_poller import SQSPoller
from src.forecast.application.forecast_service import ForecastService
from src.forecast.application.loader import StationLoaderModels


@dataclass
class DependencyInjection:
    poller: Poller = field(default=None)
    forecaster: ForecastUseCase = field(default=None)

    def __post_init__(self):
        self.poller = self.get_poller()
        self.forecaster = self.get_forecaster()

    def get_poller(self):
        return SQSPoller()

    def get_forecaster(self):
        return ForecastService(loader=StationLoaderModels())
