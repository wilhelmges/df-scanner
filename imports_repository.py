import sqlite3
from pathlib import Path

DB_PATH = Path("df.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def file_processed(file_hash: str) -> bool:
    """
    Перевіряє, чи є файл з таким хешем у БД.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM imports WHERE file_hash = ? LIMIT 1",
            (file_hash,)
        )
        return cursor.fetchone() is not None


def add_file(file_hash: str, file_name: str, status: str = "new") -> int:
    """
    Додає запис про файл.
    Повертає ID нового запису.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO imports (
                file_hash,
                file_name,
                status
            )
            VALUES (?, ?, ?)
            """,
            (file_hash, file_name, status)
        )
        conn.commit()
        return cursor.lastrowid