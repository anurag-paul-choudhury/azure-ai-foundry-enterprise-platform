
import sqlite3
from datetime import datetime, timezone

DATABASE_PATH = "monitoring/telemetry.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            model TEXT,

            latency REAL,

            prompt_tokens INTEGER,

            completion_tokens INTEGER,

            total_tokens INTEGER,

            status TEXT

        )
    """)

    connection.commit()
    connection.close()


def log_request(result):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO requests (

            timestamp,
            model,
            latency,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        datetime.now(timezone.utc).isoformat(),
        result.get("model"),
        result.get("latency"),
        result.get("prompt_tokens"),
        result.get("completion_tokens"),
        result.get("total_tokens"),
        result.get("status")

    ))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Telemetry database initialized successfully.")
