from fastapi import FastAPI
from pydantic import BaseModel
from .db import get_connection
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ STATIC FILES ------------------
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
def join():
    return FileResponse(os.path.join(BASE_DIR, "static", "join.html"))

@app.get("/profile")
def profile():
    return FileResponse(os.path.join(BASE_DIR, "static", "profile.html"))

@app.get("/dashboard")
def dashboard():
    return FileResponse(os.path.join(BASE_DIR, "static", "dashboard.html"))

# ------------------ MODELS ------------------
class JoinRequest(BaseModel):
    code: str
    nickname: str

class AnswerRequest(BaseModel):
    question_id: int
    student_id: int
    participant_id: int
    answer: str

# ------------------ STUDENT JOIN ------------------
@app.post("/api/join")
def join_class(data: JoinRequest):
    conn = get_connection()
    cur = conn.cursor()

    # find active session
    cur.execute(
        "SELECT id FROM sessions WHERE code=%s AND is_active=true",
        (data.code,)
    )
    session = cur.fetchone()
    if not session:
        cur.close()
        conn.close()
        return {"error": "Invalid code"}

    session_id = session[0]

    # create student
    cur.execute(
        "INSERT INTO students (display_name) VALUES (%s) RETURNING id",
        (data.nickname,)
    )
    student_id = cur.fetchone()[0]

    # create participant
    cur.execute(
        """
        INSERT INTO participants (session_id, student_id, nickname)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (session_id, student_id, data.nickname)
    )
    participant_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {
        "student_id": student_id,
        "participant_id": participant_id,
        "session_id": session_id
    }

# ------------------ GET ACTIVE QUESTION ------------------
@app.get("/api/question/{session_id}")
def get_question(session_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # auto-close expired questions
    cur.execute(
        """
        SELECT
            id,
            text,
            is_open,
            auto_close_at,
            (auto_close_at IS NOT NULL AND auto_close_at < NOW()) AS is_timed_out
        FROM questions
        WHERE session_id=%s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (session_id,)
    )

    q = cur.fetchone()
    if not q:
        cur.close()
        conn.close()
        return {"id": None, "timed_out": False}

    question_id, question_text, is_open, auto_close_at, is_timed_out = q

    if is_timed_out and is_open:
        cur.execute(
            "UPDATE questions SET is_open=false WHERE id=%s",
            (question_id,)
        )
        is_open = False

    conn.commit()
    cur.close()
    conn.close()

    if is_timed_out:
        return {
            "id": None,
            "timed_out": True,
            "message": "Timeout question",
        }


    if not is_open:
        return {"id": None, "timed_out": False}

    return {
        "id": question_id,
        "text": question_text,
        "timed_out": False,
        "timeout_at": auto_close_at.isoformat() if auto_close_at else None,
    }


# ------------------ SUBMIT ANSWER ------------------
@app.post("/api/answer")
def submit_answer(data: AnswerRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT is_open, auto_close_at,
               (auto_close_at IS NOT NULL AND auto_close_at < NOW()) AS is_timed_out
        FROM questions
        WHERE id=%s
        """,
        (data.question_id,)
    )
    question_row = cur.fetchone()
    if not question_row:
        cur.close()
        conn.close()
        return {"status": "error", "message": "Question not found"}

    is_open, auto_close_at, is_timed_out = question_row
    if is_timed_out and is_open:
        cur.execute(
            "UPDATE questions SET is_open=false WHERE id=%s",
            (data.question_id,)
        )
        is_open = False

    if is_timed_out or not is_open:
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "timeout", "message": "Timeout question"}

    cur.execute(
        """
        INSERT INTO answers
        (question_id, student_id, participant_id, answer_text)
        VALUES (%s, %s, %s, %s)
        """,
        (data.question_id, data.student_id, data.participant_id, data.answer)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}

# ------------------ LIVE ANSWERS ------------------
@app.get("/api/answers/{question_id}")
def get_answers(question_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            a.id,
            COALESCE(p.nickname, s.display_name),
            a.answer_text,
            a.starred
        FROM answers a
        LEFT JOIN participants p ON p.id = a.participant_id
        LEFT JOIN students s ON s.id = a.student_id
        WHERE a.question_id = %s
        ORDER BY a.submitted_at DESC
        """,
        (question_id,)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "text": r[2],
            "starred": r[3],
        }
        for r in rows
    ]


@app.post("/api/star/{answer_id}")
def toggle_star(answer_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE answers SET starred = NOT starred WHERE id = %s",
        (answer_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}

@app.post("/api/student/profile")
def save_profile(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE students SET display_name=%s WHERE id=%s",
        (data["full_name"], data["student_id"])
    )

    cur.execute(
        "UPDATE participants SET nickname=%s WHERE id=%s",
        (data["full_name"], data["participant_id"])
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "ok"}

@app.post("/api/question/start")
def start_question():
    # logic start question
    return {"status": "started"}

@app.post("/api/question/close")
def close_question():
    # logic close question
    return {"status": "closed"}
