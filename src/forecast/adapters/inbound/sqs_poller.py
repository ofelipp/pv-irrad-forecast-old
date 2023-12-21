# ! ./venv/bin/python3.10

import boto3
import numpy as np

from src.domain.data import Data
from src.forecast.ports.inbound.poller import Poller

TEST_MESSAGES = [
    Data("job_ulid", "message_from_queue", np.array([0, 0, 0])),
    Data("job_ulid", "message_from_queue", np.array([0, 0, 1])),
    Data("job_ulid", "message_from_queue", np.array([0, 1, 0])),
    Data("job_ulid", "message_from_queue", np.array([0, 1, 1])),
    Data("job_ulid", "message_from_queue", np.array([1, 0, 0])),
]


class SQSPoller(Poller):
    """SQS Poller: get job from SQS and transform into Data to Forecast"""

    def __init__(self):
        # self.__client = boto3.client("sqs")
        # self.queues = {"queue_name": "queue_url"}
        self.__messages = TEST_MESSAGES

    def get_job(self, queue_name: str) -> Data:
        return self.__messages.pop(0)

    def have_job(self, queue_name: str) -> bool:
        return len(self.__messages) > 0
