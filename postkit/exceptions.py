import requests as _r


class PostkitError(Exception):
    pass


class RequireError(PostkitError):
    pass


class LoaderError(PostkitError):
    pass


class BadResponse(PostkitError):
    def __init__(self, resp: _r.Response, message: str = None):
        message = f'HTTP code = {resp.status_code}' if message is None else message
        super().__init__(message)
        self.response = resp
