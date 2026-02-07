try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # Python <=3.10

from pathlib import Path


def load_extensions(config_path: Path, group: str) -> set[str]:
    with config_path.open("rb") as f:
        data = tomllib.load(f)

    if group not in data:
        raise ValueError(f"Unknown file group: {group}")

    return {ext.lower() for ext in data[group]["extensions"]}