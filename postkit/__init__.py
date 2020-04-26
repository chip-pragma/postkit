import typing as T
from pathlib import Path


def storage_dir(path: T.Union[str, Path] = '') -> Path:
    path = Path(path) if isinstance(path, str) else path
    if path.is_absolute():
        return path
    return Path.home() / '.postkit' / path


sd = storage_dir


def init():
    sd_path = storage_dir()
    if not sd_path.exists():
        storage_dir().mkdir(parents=True)
