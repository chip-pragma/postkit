import typing as T
import requests as _r
from furl import furl
from postkit.service import ServiceConfig, Route, BasePrep
from postkit.service.loader import BaseLoader


class BaseService:
    __api__ = ''
    __tag__ = ''

    @classmethod
    def load_config(cls, loader: BaseLoader, host: str, env: str) -> ServiceConfig:
        return loader.load_config(
            '.'.join([cls.__api__, cls.__tag__, host, env])
        )

    def __init__(self, config: ServiceConfig):
        if not self.__api__ or not self.__tag__:
            raise NameError('"api" nor "tag" not defined')
        if config.api != self.__api__ or config.tag != self.__tag__:
            raise NameError(f'Wrong environment <{config}> used for service <{self}>')

        self.config = config

    def __str__(self):
        return f'{self.__api__}.{self.__tag__}'

    def _route(self,
               url_name: str,
               method: str,
               path: str = None,
               *,
               query: T.Mapping[str, str] = None,
               headers: T.Mapping[str, str] = None,
               json: T.Mapping[str, T.Any] = None,
               preps: T.Iterable[BasePrep] = None,
               handler: T.Callable[[_r.Response], T.Any] = None):
        # args
        path = '' if path is None else path
        query = {} if query is None else query
        headers = {} if headers is None else headers
        preps = [] if not preps else preps

        # url
        url_obj = self.config.urls[url_name].copy()
        url_obj.path /= path

        # preps
        for p in preps:
            headers = p.header(headers)
            query = p.query(query)

        # query
        url_obj.query.set(query)

        # json
        if json is not None:
            headers['Content-Type'] = 'application/json'

        # route
        route = Route(
            method=method,
            url=url_obj.url,
            headers=headers,
            json=json,
            handler=handler)

        # cast for type hints
        return route
