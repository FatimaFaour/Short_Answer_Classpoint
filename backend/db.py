import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="short_ans_classpoint",
        user="postgres",
        password="ahmad1807",
        host="localhost",
        port="5432"
    )
