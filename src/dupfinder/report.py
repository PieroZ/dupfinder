from pathlib import Path
from collections import defaultdict


def generate_html(dupes: dict[str, list[Path]], output: Path):
    html = ["<html><body><h1>Duplicate Files</h1>"]

    for h, paths in dupes.items():
        html.append(f"<h2>Hash: {h}</h2><ul>")
        for p in paths:
            html.append(f"<li>{p}</li>")
        html.append("</ul>")

    html.append("</body></html>")
    output.write_text("\n".join(html), encoding="utf-8")
