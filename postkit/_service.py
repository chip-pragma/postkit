import typing as t

from postkit import _utils
from postkit._utils import INHERIT, InheritType
from postkit.exceptions import LoadError, HandleError
from postkit.loader._base import BaseLoader
from postkit._config import ServiceConfig
from postkit._printer import RoutePrinter
from postkit._route import Route

Handler = t.Callable[[Route], Route]


class BaseService:
    __api__ = ''
    __tag__ = ''

    @classmethod
    def load_config(cls, loader: BaseLoader, host: str, env: str) -> ServiceConfig:
        return loader.load_config(
            '.'.join([cls.__api__, cls.__tag__, host, env])
        )

    def __init__(self, config: ServiceConfig, printer: RoutePrinter):
        if not self.__api__ or not self.__tag__:
            raise NameError('"api" nor "tag" not defined')
        if config.api != self.__api__ or config.tag != self.__tag__:
            raise NameError(f'Wrong environment <{config}> used for service <{self}>')

        self.config = config
        self.printer = printer
        self.handlers: t.List[Handler] = []

    def __str__(self):
        return f'{self.__api__}.{self.__tag__}.{self.config.host}.{self.config.env}'

    def _route(self,
               url_name: str,
               method: str = None,
               path: str = None,
               match: dict = None,
               query: dict = None,
               headers: dict = None,
               json: dict = None,
               handlers: t.List[t.Union[Handler, InheritType]] = INHERIT,
               name: str = None,
               printer: RoutePrinter = INHERIT
               ):
        printer, _ = _utils.resolve_inherit(printer, self.printer)
        handlers, default_handlers = _utils.resolve_inherit(handlers, self.handlers)

        try:
            url_obj = self.config.urls[url_name].copy()
        except KeyError as e:
            raise LoadError(f'URL "{url_name}" not found') from e

        route = Route(
            method=method,
            url=url_obj.tostr(),
            path=path,
            match=match,
            query=query,
            headers=headers,
            json_=json,
            name=name,
            printer=printer
        )

        if not default_handlers:
            try:
                ellipsis_handler_idx = handlers.index(...)
                handlers.pop(ellipsis_handler_idx)
                handlers += self.handlers
            except ValueError:
                pass

        handler_idx = 0
        try:
            for idx, handler in enumerate(handlers):
                handler_idx = idx
                route = handler(route)
        except Exception as e:
            raise HandleError(f'"[{handler_idx}]{handlers[handler_idx]} raised error"') from e

        return route
