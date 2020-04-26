import typing as T
from postkit.core.config import ServiceConfig
from furl import furl
from postkit.core.route import Route
from postkit.core.prep import BasePrep


class BaseService:
    __api__ = ''
    __tag__ = ''

    @classmethod
    def config(cls, host: str, env: str):
        return '.'.join(
            [cls.__api__, cls.__tag__, host, env]
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
               preps: T.Iterable[BasePrep] = None) -> Route:
        # args
        query = {} if query is None else query
        headers = {} if headers is None else headers
        json = {} if json is None else json
        preps = [] if not preps else preps

        # url
        url_obj = self.config.urls[url_name].copy()
        url_obj.path /= path

        # preps
        for p in preps:
            headers = p.header(headers)
            query = p.query(query)
            json = p.json(json)

        # query
        url_obj.query.set(query)

        # route
        route = Route(
            method=method,
            url=url_obj.url,
            headers=headers,
            json=json)

        return route
