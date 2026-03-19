import os
from typing import Any

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()


def _db_settings() -> dict[str, Any]:
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "bi_dw"),
        "user": os.getenv("DB_USER", "bi_user"),
        "password": os.getenv("DB_PASSWORD", "bi_pass"),
    }


def fetch_all(sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    with psycopg.connect(**_db_settings(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            return list(cur.fetchall())