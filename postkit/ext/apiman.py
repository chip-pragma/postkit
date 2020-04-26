from postkit.core.prep import BasePrep
from postkit.core.config import ServiceConfig


class ApimanPrep(BasePrep):
    def __init__(self, config: ServiceConfig):
        self.apikey = config.vars.get('apikey')
        if not self.apikey:
            raise KeyError(f'Apikey not found in <{config}>')

    def header(self, src: dict) -> dict:
        src.update(
            {'X-API-Key': self.apikey}
        )
        return src
