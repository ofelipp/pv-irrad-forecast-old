"""
Program to forecast radiance curve for Brazilian energy system, located in
Santo Andre. The data are retrieved from SEMASA meteorologic stations and UFABC
Solar Project.

Author: ofelippm (felippe.matheus@aluno.ufabc.edu.br)
"""
import time

from src.forecast.ports.inbound.poller import Poller
from src.forecast.ports.inbound.forecast_use_case import ForecastUseCase
from src.forecast.dependency_injection import DependencyInjection

dep_inj = DependencyInjection()
poller, forecaster = dep_inj.poller, dep_inj.forecaster


class Main:
    def __init__(self, poller: Poller, forecaster: ForecastUseCase):
        self.poller = poller
        self.forecaster = forecaster

    def run_forecast(self):
        while self.poller.have_job("queue"):
            job = self.poller.get_job("queue")
            print(f"Job: {job}")

            forecast = self.forecaster.predict(X=job)
            print(f"Forecast: {forecast}")


if __name__ == "__main__":
    main = Main(poller, forecaster)
    main.run_forecast()
