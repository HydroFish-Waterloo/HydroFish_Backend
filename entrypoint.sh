#!/bin/bash

set -euo pipefail

wait_for_db() {
    python << END
import sys
import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="${DB_HOST}",
        port=3306,
        user="${DB_USER}",
        password="${DB_PASSWORD}",
        database="${DB_NAME}"
    )


    if conn.is_connected():
        print("MySQL is connected.")
        conn.close()
except Error as e:
    print("Waiting for database connection...")
    sys.exit(-1)
END
}

until wait_for_db; do
    >&2 echo "Waiting for MYSQL to become available..."
    sleep 5
done

python manage.py makemigrations
python manage.py migrate --noinput

exec "$@"