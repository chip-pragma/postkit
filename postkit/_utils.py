import os
import typing as t
import json

TResolved = t.TypeVar('TResolved')


class InheritType:
    def __eq__(self, other):
        return True


INHERIT = InheritType()


def curl(method: str, url: str, headers: dict, json_: dict = None) -> str:
    # TODO correct width format

    space = ' \\\n'

    # curl
    parts = [
        f"curl --location",
        f"--request {method}",
        f"'{url}'"
    ]
    # header
    if headers:
        parts += [
            f"--header '{k}: {v}'"
            for k, v in headers.items()
        ]
    # data
    if json_:
        data = json.dumps(json_, indent=2)
        parts.append(f"--data-raw '{data}'")

    # result
    full = space.join(parts)
    return full


def resolve_inherit(source: TResolved, default: TResolved) -> t.Tuple[TResolved, bool]:
    if source == INHERIT:
        return default, True
    return source, False
