import typing as T
import requests as _r
import json

TResponse = T.TypeVar('TResponse')


class Route(T.Generic[TResponse]):
    def __init__(self, method: str, url: str, headers: dict = None, json_: str = None,
                 *, handler: T.Callable[[_r.Response], TResponse] = None):
        self.method = method
        self.url = url
        self.headers = headers
        self.json = json_

        self.handler = self._default_handler if handler is None else handler

    def call(self) -> TResponse:
        return self.handler(
            _r.request(self.method, self.url, headers=self.headers, json=self.json)
        )

    def pure(self) -> _r.Response:
        return _r.request(self.method, self.url, headers=self.headers, json=self.json)

    def to_curl(self):
        space = ' \\\n'

        # curl
        parts = [
            f"curl --location{space}--request {self.method} '{self.url}'"
        ]
        # header
        if self.headers:
            headers = space.join([
                f"--header '{k}: {v}'"
                for k, v in self.headers.items()
            ])
            parts.append(headers)
        # data
        if self.json:
            data = json.dumps(self.json, indent=2)
            parts.append(f"--data-raw '{data}'")

        # result
        full = space.join(parts)
        return full

    @classmethod
    def _default_handler(cls, resp: _r.Response) -> TResponse:
        return resp


ResponseRoute = Route[_r.Response]
