# ! ./venv/bin/python3.10

from src.domain.data import Data
from src.forecast.ports.outbound.object_storage import ObjectStorage


class S3ObjectStorage(ObjectStorage):
    def put_object(self, data: Data, path: str):
        raise NotImplementedError()
