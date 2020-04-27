import typing as T
from pathlib import Path
import yaml
from furl import furl
from postkit.exceptions import LoaderError
from postkit.service.loader import BaseLoader
from postkit.service import ServiceConfig


class _K:
    API = 'API'
    TAG = 'TAG'
    HOST = 'HOST'
    ENV = 'ENV'
    URL = 'URL'
    FILE = 'FILE'
    VAR = 'VAR'


def _key_field(d: dict, key: str):
    value = d.get(key)
    if not value:
        raise LoaderError(f'Field <{key}> not defined')
    return value


def _value_field(d: dict, key: str, name: str):
    value = d.get(key)
    if not value:
        raise LoaderError(f'{name} <{key}> not found')
    return value


class YamlLoader(BaseLoader):
    def __init__(self, file: T.Union[str, Path]):
        super().__init__()

        file_path = Path(file) if isinstance(file, str) else file
        with file_path.open('r') as f:
            self.raw = yaml.load(f, yaml.SafeLoader)

        self.root_dir = file_path.parent

    def load_config(self, name: str) -> ServiceConfig:
        api, tag, host, env = self.split_config_name(name)
        config = ServiceConfig(api, tag, host, env)

        # global
        self._update_config(config, self.raw)
        # api
        api_list = _key_field(self.raw, _K.API)
        api_lvl = _value_field(api_list, api, 'Api')
        self._update_config(config, api_lvl)
        # tag
        tag_list = _key_field(api_lvl, _K.TAG)
        tag_lvl = _value_field(tag_list, tag, 'Tag')
        self._update_config(config, tag_lvl)
        # host
        host_list = _key_field(tag_lvl, _K.HOST)
        host_lvl = _value_field(host_list, host, 'Host')
        self._update_config(config, host_lvl)
        # env
        env_list = _key_field(host_lvl, _K.ENV)
        env_lvl = _value_field(env_list, env, 'Environment')
        self._update_config(config, env_lvl)

        # result
        return config

    def _update_config(self, config: ServiceConfig, level: dict):
        urls: dict = level.get(_K.URL)
        if urls:
            for name, url in urls.items():
                config.urls[name] = furl(url)

        files: dict = level.get(_K.FILE)
        if files:
            for name, file in files.items():
                file_path = Path(file)
                if not file_path.is_absolute():
                    file_path = self.root_dir / file_path
                if not file_path.exists():
                    raise FileExistsError(f'File <{file}> not exists in <{config}>')
                config.files[name] = file_path

        vars_: dict = level.get(_K.VAR)
        if vars_:
            config.vars.update(vars_)
