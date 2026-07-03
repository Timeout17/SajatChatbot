"""
Az adatbátisö összekötetés itt zajlik, itt csak összekötés van, más nem
"""

import sqlite3
from pathlib import Path

class DatabaseConnectionClass:

    def __init__(self, base_dir: Path):
        self.db_path: Path = base_dir / "data" / "rag.sqlite" # a fájlnak az ut vonala
        self.db_path.parent.mkdir( # létrehozza a mappát ha még nem létezik
            parents=True, # ha hiányzik a többi mappa is, akkor azokat is létrehozza
            exist_ok=True # ha elve létezik akkor nem dob hibát
        )

    def connect(self):
        """
        Az összekötés itt történik
        """
        conn = sqlite3.connect(self.db_path) # kapcsolódik az adatbázishoz, és ha nincsen ilyen fájl, akkor létrehozza
        conn.row_factory = sqlite3.Row # hogy ne számokkal, hanem szavakkal indexeljünk
        conn.execute("PRAGMA foreign_keys = ON;") # be kapcsoljuk a külső kulcsoakt, mert elve ki vannak kapcsolva
        print("Connected to DB:", self.db_path)

        return conn
    
    def close(self, conn: sqlite3.Connection):
        conn.close() # le zárja az adatbázis kapcsolatot