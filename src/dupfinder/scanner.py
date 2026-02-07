import os
from pathlib import Path
from collections import defaultdict
from models import FileEntry


def scan_directory(root: Path, allowed_exts: set[str]) -> list[FileEntry]:
    files = []

    def _scan(dir_path: Path):
        with os.scandir(dir_path) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    _scan(Path(entry.path))
                elif entry.is_file():
                    ext = Path(entry.name).suffix.lower()
                    if ext in allowed_exts:
                        stat = entry.stat()
                        files.append(FileEntry(
                            path=Path(entry.path),
                            size=stat.st_size,
                            mtime=stat.st_mtime
                        ))

    _scan(root)
    return files


def group_by_size(files):
    groups = defaultdict(list)
    for f in files:
        groups[f.size].append(f)
    return {k: v for k, v in groups.items() if len(v) > 1}
