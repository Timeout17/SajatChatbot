"""
Az adatbátisö összekötetés itt zajlik, itt csak összekötés van, más nem
"""

import sqlite3
from pathlib import Path

class SQLConnectionClass:

    def __init__(self, base_dir: Path):
        self.db_path: Path = base_dir / "data" / "rag.sqlite"

    def sql_connection(self):
        """
        Az összekötés itt történik
        """
        conn = sqlite3.connect(self.db_path)
        print("Connected to DB:", self.db_path)
        conn.close()