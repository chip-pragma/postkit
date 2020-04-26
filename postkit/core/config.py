import typing as T
from pathlib import Path
from furl import furl


class ServiceConfig:
    def __init__(self, api: str, tag: str, host: str, env: str):
        self.api = api
        self.tag = tag
        self.host = host
        self.env = env

        self.files: T.Dict[str, Path] = {}
        self.urls: T.Dict[str, furl] = {}
        self.vars: T.Dict[str, T.Any] = {}

    def __str__(self):
        return f'{self.api}.{self.tag}.{self.host}.{self.env}'
