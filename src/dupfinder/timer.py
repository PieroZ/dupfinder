import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"[TIME] {label}: {end - start:.2f}s")
