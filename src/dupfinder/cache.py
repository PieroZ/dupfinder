import sqlite3
from pathlib import Path


class Cache:
    def __init__(self, db_path: Path):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            size INTEGER,
            mtime REAL,
            hash TEXT
        )
        """)
        self.conn.commit()

    def get_hash(self, path: Path, size: int, mtime: float) -> str | None:
        row = self.conn.execute(
            "SELECT hash FROM files WHERE path=? AND size=? AND mtime=?",
            (str(path), size, mtime)
        ).fetchone()
        return row[0] if row else None

    def update(self, path: Path, size: int, mtime: float, hash_value: str):
        self.conn.execute("""
        INSERT OR REPLACE INTO files (path, size, mtime, hash)
        VALUES (?, ?, ?, ?)
        """, (str(path), size, mtime, hash_value))
        self.conn.commit()
