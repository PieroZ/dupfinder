from collections import defaultdict
from pathlib import Path

from .models import FileEntry


def scan_directory(root: Path) -> list[FileEntry]:
    entries = []
    for path in root.rglob("*"):
        if path.is_file():
            stat = path.stat()
            entries.append(FileEntry(
                path=path,
                size=stat.st_size,
                mtime=stat.st_mtime
            ))
    return entries


def group_by_size(files: list[FileEntry]):
    groups = defaultdict(list)
    for f in files:
        groups[f.size].append(f)
    return {k: v for k, v in groups.items() if len(v) > 1}
