from ..connect import run_query

def get_teacher_by_email(email):
    return run_query(
        "SELECT id, name FROM teachers WHERE email=%s",
        [email],
        fetch=True
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
