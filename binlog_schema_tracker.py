import json
import hashlib
import os
import tempfile
from filelock import FileLock
import mysql.connector
from db import get_connection
from logger import logger
import time

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import QueryEvent


SCHEMA_FILE = "schema_store/schema.json"
LOCK_FILE = "schema_store/schema.json.lock"

MYSQL_SETTINGS = {
    "host": "localhost",
    "port": 3306,
    "user": "mcp_user",
    "passwd": "AirtelAI@#1"
}

EXCLUDED_DBS = {
    "mysql",
    "sys",
    "performance_schema",
    "information_schema"
}


def fetch_schema():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            TABLE_SCHEMA,
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    schema = {}

    for row in rows:

        db = row["TABLE_SCHEMA"]

        if db in EXCLUDED_DBS:
            continue

        table = row["TABLE_NAME"]

        schema.setdefault(db, {})
        schema[db].setdefault(table, [])

        schema[db][table].append({
            "column": row["COLUMN_NAME"],
            "type": row["DATA_TYPE"],
            "nullable": row["IS_NULLABLE"],
            "key": row["COLUMN_KEY"]
        })

    return schema


def compute_hash(data):

    return hashlib.md5(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()


def atomic_write(data, file_path):

    dir_name = os.path.dirname(file_path) or "."

    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=dir_name
    ) as tmp:

        json.dump(data, tmp, indent=2)

        temp_name = tmp.name

    os.replace(temp_name, file_path)


def update_schema_file(schema):

    lock = FileLock(LOCK_FILE)

    with lock:
        time.sleep(20)
        atomic_write(schema, SCHEMA_FILE)


def load_existing_hash():

    if not os.path.exists(SCHEMA_FILE):
        return None

    with open(SCHEMA_FILE, "r") as f:
        data = json.load(f)

    return compute_hash(data)


def is_schema_query(query):

    query = query.upper()

    ddl_keywords = [
        "CREATE",
        "ALTER",
        "DROP",
        "TRUNCATE",
        "RENAME"
    ]

    return any(keyword in query for keyword in ddl_keywords)


def start_listener():

    logger.info("Starting MySQL binlog schema tracker...")

    last_hash = load_existing_hash()

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=100,
        blocking=True,
        only_events=[QueryEvent]
    )

    for event in stream:

        query = event.query.strip()

        schema = event.schema

        if schema in EXCLUDED_DBS:
            continue

        if is_schema_query(query):

            logger.info(f"Schema change detected | Database={schema} | Query={query}")

            try:

                latest_schema = fetch_schema()

                current_hash = compute_hash(latest_schema)

                if current_hash != last_hash:

                    update_schema_file(latest_schema)

                    last_hash = current_hash

                    logger.info("Schema file updated successfully")

                else:
                    logger.info("No actual schema difference detected")

            except Exception as e:
                logger.error(f"Schema update failed : {e}")

    stream.close()


if __name__ == "__main__":
    start_listener()
