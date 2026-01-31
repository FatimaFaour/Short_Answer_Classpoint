from ..connect import run_query

def get_teacher_by_email(email):
    return run_query(
        "SELECT id, name FROM teachers WHERE email=%s",
        [email],
        fetch=True
    )
def get_common_answers(question_id, limit=5):
    query = """
        SELECT
            LOWER(TRIM(answer_text)) AS answer,
            COUNT(*) AS count
        FROM answers
        WHERE question_id = %s
          AND answer_text IS NOT NULL
          AND TRIM(answer_text) <> ''
        GROUP BY LOWER(TRIM(answer_text))
        HAVING COUNT(*) > 1
        ORDER BY count DESC
        LIMIT %s
    """
    rows = run_query(query, [question_id, limit], fetch=True)
    return rows or []
def get_starred_answers(question_id, limit=5):
    query = """
        SELECT answer_text
        FROM answers
        WHERE question_id = %s
          AND starred = TRUE
          AND answer_text IS NOT NULL
          AND TRIM(answer_text) <> ''
        LIMIT %s
    """
    rows = run_query(query, [question_id, limit], fetch=True)
    return [r[0] for r in rows] if rows else []

def get_quality_breakdown(question_id):
    query = """
        SELECT
            COUNT(*) FILTER (WHERE LENGTH(answer_text) >= 40) AS clear,
            COUNT(*) FILTER (
                WHERE LENGTH(answer_text) BETWEEN 20 AND 39
            ) AS partial,
            COUNT(*) FILTER (WHERE LENGTH(answer_text) < 20) AS weak
        FROM answers
        WHERE question_id = %s
          AND answer_text IS NOT NULL
          AND TRIM(answer_text) <> ''
    """
    rows = run_query(query, [question_id], fetch=True)

    if not rows:
        return 0, 0, 0

    return rows[0]

def get_answer_stats(question_id):
    query = """
        SELECT
            COUNT(*) AS answered,
            COUNT(*) FILTER (WHERE starred = TRUE) AS starred,
            COUNT(DISTINCT LOWER(TRIM(answer_text))) AS unique_answers
        FROM answers
        WHERE question_id = %s
          AND answer_text IS NOT NULL
          AND TRIM(answer_text) <> ''
    """
    rows = run_query(query, [question_id], fetch=True)

    if not rows:
        return 0, 0, 0, 0

    answered, starred, unique_answers = rows[0]

    avg_time = 0  # placeholder until timestamps exist
    return answered, starred, avg_time, unique_answers


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

def create_question(session_id, text, timeout_seconds=None):
    return run_query(
        """
        INSERT INTO questions (session_id, text, is_open, auto_close_at)
        VALUES (
            %s,
            %s,
            true,
            CASE
                WHEN %s IS NULL THEN NULL
                ELSE NOW() + (%s * INTERVAL '1 second')
            END
        )
        RETURNING id
        """,
        [session_id, text, timeout_seconds, timeout_seconds],
        fetch=True
    )[0][0]

def get_common_answers(question_id, limit=5):
    query = """
        SELECT 
            answer_text,
            COUNT(*) AS count
        FROM answers
        WHERE question_id = %s
          AND answer_text IS NOT NULL
          AND TRIM(answer_text) <> ''
        GROUP BY answer_text
        HAVING COUNT(*) > 1
        ORDER BY count DESC
        LIMIT %s
    """
    rows = run_query(query, [question_id, limit], fetch=True)
    return rows or []

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
