import requests as r
import furl

from postkit import _utils
from postkit._utils import INHERIT
from postkit._printer import RoutePrinter


class Route:
    def __init__(self,
                 method: str = None,
                 url: str = None,
                 path: str = None,
                 match: dict = None,
                 query: dict = None,
                 headers: dict = None,
                 json_: dict = None,
                 name: str = None,
                 printer: RoutePrinter = None
                 ):
        self.method = method
        self.url = url
        self.path = path
        self.headers = {} if headers is None else headers
        self.match = {} if match is None else match
        self.query = {} if query is None else query
        self.json = json_
        self.name = name
        self.printer = printer

    def furl(self) -> furl.furl:
        furl_ = furl.furl(url=self.url)

        if self.path:
            path = self.path
            if self.match:
                path = path.format(**self.match)
            furl_.add(path=path)

        if self.query:
            furl_.query.set(self.query)

        return furl_

    def call(self, except_=True, printer: RoutePrinter = INHERIT) -> r.Response:
        printer, _ = _utils.resolve_inherit(printer, self.printer)

        try:
            url = self.furl().tostr()

            if printer:
                name = self.name if self.name else f'{self.method} {self.path}'
                printer.request(name, self.method, url, self.headers, self.json)

            response = r.request(self.method, url, headers=self.headers, json=self.json)

            if printer:
                printer.response(response)

            return response
        except Exception as e:
            if except_:
                printer.error(e)
            else:
                raise e
