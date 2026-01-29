import psycopg2

import psycopg2
from psycopg2 import sql

DB_NAME = "short_ans_classpoint"
USER = "postgres"
PASSWORD = "123456"
HOST = "localhost"
PORT = "5432"

def get_connection(dbname=DB_NAME):
    try:
        # Try connecting to the target database
        conn = psycopg2.connect(
            dbname=dbname,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        # If the database does not exist, create it
        if "does not exist" in str(e):
            # Connect to default database
            conn = psycopg2.connect(
                dbname="postgres",
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0").format(
                sql.Identifier(DB_NAME)
            ))

            cur.close()
            conn.close()
            # Now try connecting again
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            return conn
        else:
            raise

def run_query(sql, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or [])
    data = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return data
