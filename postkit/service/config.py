import typing as T
from pathlib import Path
from furl import furl
from postkit.exceptions import RequireError


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

    def require_url(self, name: str) -> furl:
        if name not in self.urls:
            raise RequireError(f'URL <{name}> is require in <{self}>')
        return self.urls[name]

    def require_file(self, name: str) -> Path:
        if name not in self.files:
            raise RequireError(f'File <{name}> is require in <{self}>')
        return self.files[name]

    def require_var(self, name: str, type_: T.Optional[T.Type] = None) -> T.Any:
        if name not in self.vars:
            raise RequireError(f'Variable <{name}> is require in <{self}>')
        if type_ and not isinstance(self.vars[name], type_):
            raise RequireError(f'Variable <{name}> in <{self}> must be <{type_}>')
        return self.vars[name]

