import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="short_ans_classpoint",
        user="postgres",
        password="ahmad1807"
    )

    print("✅ Database connection established.")

    # Try reading data
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user;")
    result = cur.fetchall()
    print("📘 Current database and user:")
    print(result)

    cur.close()
    conn.close()
    print("🔌 Connection closed successfully.")

except Exception as e:
    print("❌ Error occurred:", e)
    if conn:
        conn.close()
        print("🔌 Connection closed due to error.")