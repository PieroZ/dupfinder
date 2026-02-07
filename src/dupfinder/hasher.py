import hashlib
from pathlib import Path

PARTIAL_SIZE = 64 * 1024


def partial_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        h.update(f.read(PARTIAL_SIZE))
        f.seek(max(0, path.stat().st_size - PARTIAL_SIZE))
        h.update(f.read(PARTIAL_SIZE))
    return h.hexdigest()


def full_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
