import abc
import postkit
from postkit.core.config import ServiceConfig


class BaseLoader(abc.ABC):
    def __init__(self):
        self.root_dir = postkit.storage_dir()

    @abc.abstractmethod
    def load_config(self, name: str) -> ServiceConfig:
        raise NotImplementedError()

    @classmethod
    def split_config_name(cls, name: str):
        s = tuple(name.split('.'))
        if len(s) != 4:
            raise ValueError(f'Incorrect config name "{name}"')
        return s

    @abc.abstractmethod
    def _update_config(self, config: ServiceConfig, level: dict):
        raise NotImplementedError()
