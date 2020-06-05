from postkit._route import Route
from postkit._service import ServiceConfig


class ApimanHandler:
    HEADER = 'header'
    QUERY = 'query'

    def __init__(self, config: ServiceConfig, target=HEADER, host_name='apiman'):
        self.target = target

        self._enabled = (host_name == config.host)

        if self._enabled:
            self.apikey = config.require_var('apikey', str)

    def __call__(self, route: Route) -> Route:
        if self._enabled:
            if self.HEADER == self.target:
                route.headers.update({'X-API-Key': self.apikey})
            elif self.QUERY == self.target:
                route.headers.update({'apikey': self.apikey})

        return route
