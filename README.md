# Duplicate Finder

CLI tool for finding duplicate files on Windows using size + hashing strategy.

## Features
- Recursive directory scan
- SQLite cache (file size + mtime + hash)
- Partial + full hashing
- HTML report

## Setup

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -e .
