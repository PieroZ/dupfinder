# Duplicate Finder

CLI tool for finding duplicate files on Windows using size + hashing strategy.

## Features

- Recursive directory scan (optimized with os.scandir)
- File filtering by extension groups (configurable)
- Partial + full hashing
- SQLite cache
- Multi-threaded hashing
- Built-in performance timing
- HTML report

## File Groups

Define file groups in TOML:

```toml
[images]
extensions = [".png", ".jpg", ".jpeg"]

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -e .
