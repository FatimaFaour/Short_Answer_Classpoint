from ..connect import run_query

def get_teacher_by_email(email):
    return run_query(
        "SELECT id, name FROM teachers WHERE email=%s",
        [email],
        fetch=True
    )
def get_answer_stats(question_id):
    return run_query(
        """
        SELECT
            COUNT(*) AS answered,
            COUNT(*) FILTER (WHERE starred = true) AS starred
        FROM answers
        WHERE question_id = %s
        """,
        [question_id],
        fetch=True
    )[0]

def get_answers(question_id):
    return run_query(
        """
        SELECT id, text, name, starred
        FROM answers
        WHERE question_id = %s
        ORDER BY id DESC
        """,
        [question_id],
        fetch=True,
    )

def toggle_star(answer_id):
    run_query(
        "UPDATE answers SET starred = NOT starred WHERE id = %s",
        [answer_id],
    )



def create_session(teacher_id, code):
    return run_query(
        """
        INSERT INTO sessions (teacher_id, code, is_active)
        VALUES (%s, %s, true)
        RETURNING id
        """,
        [teacher_id, code],
        fetch=True
    )[0][0]

def create_question(session_id, text):
    return run_query(
        """
        INSERT INTO questions (session_id, text, is_open)
        VALUES (%s, %s, true)
        RETURNING id
        """,
        [session_id, text],
        fetch=True
    )[0][0]

def close_question(question_id):
    run_query(
        "UPDATE questions SET is_open=false WHERE id=%s",
        [question_id]
    )

def get_teacher_by_credentials(email, password):
    return run_query(
        "SELECT id, name FROM teachers WHERE email=%s AND password=%s",
        [email, password],
        fetch=True
    )

def create_teacher(name, email, password):
    return run_query(
        """
        INSERT INTO teachers (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, name
        """,
        [name, email, password],
        fetch=True
    )
