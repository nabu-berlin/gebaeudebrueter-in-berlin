import os
import sqlite3
from pathlib import Path

from .config import DEFAULT_DB_PATH


def resolve_db_path(db_path=None):
    if db_path:
        return Path(db_path)
    env_path = os.environ.get('BRUETER_DB')
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_DB_PATH)


def connect_sqlite(db_path=None, row_factory=False):
    path = resolve_db_path(db_path)
    connection = sqlite3.connect(str(path))
    if row_factory:
        connection.row_factory = sqlite3.Row
    return connection
