import requests as _r
import json


class Route:
    def __init__(self, method: str, url: str, headers: dict = None, json: str = None):
        self.method = method
        self.url = url
        self.headers = headers
        self.json = json

    def call(self) -> _r.Response:
        return _r.request(self.method, self.url, headers=self.headers, json=self.json)

    def __call__(self) -> _r.Response:
        return self.call()

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
