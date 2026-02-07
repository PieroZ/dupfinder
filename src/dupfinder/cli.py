import argparse
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from scanner import scan_directory, group_by_size
from hasher import partial_hash, full_hash
from cache import Cache
from report import generate_html
from config import load_extensions
from timer import timer


def main():
    parser = argparse.ArgumentParser("dupfinder")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--group", type=str, required=True)
    parser.add_argument("--threads", type=int, default=4)

    args = parser.parse_args()

    allowed_exts = load_extensions(args.config, args.group)
    cache = Cache(args.cache)

    with timer("Scan directory"):
        files = scan_directory(args.directory, allowed_exts)

    with timer("Group by size"):
        size_groups = group_by_size(files)

    partial_groups = defaultdict(list)
    with timer("Partial hashing"):
        for group in size_groups.values():
            for f in group:
                ph = partial_hash(f.path)
                partial_groups[(f.size, ph)].append(f)

    dupes = defaultdict(list)

    def process_file(f):
        return f, full_hash(f.path)

    with timer("Full hashing"):
        with ThreadPoolExecutor(args.threads) as ex:
            for group in partial_groups.values():
                if len(group) < 2:
                    continue

                to_hash = []
                for f in group:
                    cached = cache.get_hash(f.path, f.size, f.mtime)
                    if cached:
                        dupes[cached].append(f.path)
                    else:
                        to_hash.append(f)

                for f, h in ex.map(process_file, to_hash):
                    cache.update(f.path, f.size, f.mtime, h)
                    dupes[h].append(f.path)

    dupes = {k: v for k, v in dupes.items() if len(v) > 1}
    generate_html(dupes, args.report)


if __name__ == "__main__":
    main()