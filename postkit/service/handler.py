import requests as _r


def from_json(resp: _r.Response) -> dict:
    return resp.json()
