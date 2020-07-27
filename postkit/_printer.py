from pprint import pprint
import shutil
import json

import requests as r

from postkit import _utils


class RoutePrinter:
    STATE_UNDEFINED = -1
    STATE_REQUEST = 0
    STATE_RESPONSE = 1
    STATE_CUSTOM = 2

    def __init__(self, head=True, curl=True, headers=False, json=True):
        self.head = head
        self.curl = curl
        self.headers = headers
        self.json = json

        self.width, _ = shutil.get_terminal_size((120, 20))

        self._state = self.STATE_UNDEFINED

    def request(self, name: str, method: str, url: str, headers: dict, json: dict):
        if self.head:
            self._label(f'[{name} - REQUEST]', self.STATE_REQUEST)

        if self.curl:
            self._label('[CURL]', self.STATE_REQUEST)
            curl = _utils.curl(method, url, headers, json)
            print(curl)

    def response(self, response: r.Response):
        if self.head:
            self._label(f'[{response.status_code} - RESPONSE]', self.STATE_RESPONSE)

        if self.headers:
            self._label('[HEADERS]', self.STATE_RESPONSE)

            max_length = len(max(response.headers.keys(), key=len))
            for header, value in response.headers.items():
                print(f'{header:<{max_length}}  {value}')

        if self.json:
            self._label('[JSON]', self.STATE_RESPONSE)
            try:
                data = response.json()
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except ValueError:
                print(response.content)

    def print(self, *lines, caption='USER PRINT'):
        if self.STATE_CUSTOM != self._state:
            self._label(f'[{caption}]', self.STATE_CUSTOM)

        for line in lines:
            print(line)

    def error(self, exc: Exception):
        self._label('[EXCEPTION]', self.STATE_RESPONSE)
        print(str(exc))

    def _label(self, label: str, state: int):
        length = self.width - len(label) - 2
        sep = ' '

        if self._state != state:
            if self.STATE_REQUEST == state:
                sep = '='
            elif self.STATE_RESPONSE == state:
                sep = '-'
            elif self.STATE_CUSTOM == state:
                sep = '~'

        print(f'{sep * length} {label}')
        self._state = state
