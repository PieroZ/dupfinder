import argparse
from pathlib import Path
from collections import defaultdict

from .scanner import scan_directory, group_by_size
from .hasher import partial_hash, full_hash
from .cache import Cache
from .report import generate_html


def main():
    parser = argparse.ArgumentParser("dupfinder")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)

    args = parser.parse_args()

    cache = Cache(args.cache)
    files = scan_directory(args.directory)
    size_groups = group_by_size(files)

    partial_groups = defaultdict(list)

    for group in size_groups.values():
        for f in group:
            p_hash = partial_hash(f.path)
            partial_groups[(f.size, p_hash)].append(f)

    dupes = defaultdict(list)

    for group in partial_groups.values():
        if len(group) < 2:
            continue

        for f in group:
            cached = cache.get_hash(f.path, f.size, f.mtime)
            if cached:
                h = cached
            else:
                h = full_hash(f.path)
                cache.update(f.path, f.size, f.mtime, h)
            dupes[h].append(f.path)

    dupes = {k: v for k, v in dupes.items() if len(v) > 1}
    generate_html(dupes, args.report)

    print(f"Found {len(dupes)} duplicate groups")
