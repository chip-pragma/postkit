import typing as T


class BasePrep:
    def header(self, src: dict) -> dict:
        return src

    def query(self, src: dict) -> dict:
        return src

    def json(self, src: dict) -> dict:
        return src
