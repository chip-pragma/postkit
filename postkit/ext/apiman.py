from postkit.service import BasePrep
from postkit.service import ServiceConfig


class ApimanPrep(BasePrep):
    HEADER = 'header'
    QUERY = 'query'

    def __init__(self, config: ServiceConfig, target=HEADER):
        self.apikey = config.require_var('apikey', str)
        self.target = target

    def header(self, src: dict) -> dict:
        if self.target == self.HEADER:
            src.update(
                {'X-API-Key': self.apikey}
            )
        return src

    def query(self, src: dict) -> dict:
        if self.target == self.QUERY:
            src.update(
                {'apikey': self.apikey}
            )
        return src
