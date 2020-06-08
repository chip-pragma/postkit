import abc

from postkit.exceptions import LoadError
from postkit._config import ServiceConfig


class BaseLoader(abc.ABC):
    @abc.abstractmethod
    def load_config(self, name: str) -> ServiceConfig:
        raise NotImplementedError()

    @classmethod
    def split_config_name(cls, name: str):
        s = tuple(name.split('.'))
        if len(s) != 4:
            raise LoadError(f'Incorrect config name "{name}"')
        return s

    @abc.abstractmethod
    def _update_config(self, config: ServiceConfig, level: dict):
        raise NotImplementedError()
