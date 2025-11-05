import psycopg2

def get_connection():
    # edit these values for your setup
    return psycopg2.connect(
        dbname="short_ans_classpoint",
        user="postgres",
        password="ahmad1807",
        host="localhost",
        port="5432"
    )

# example helper
def run_query(sql, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or [])
    data = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return data
