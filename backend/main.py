from fastapi import FastAPI
from pydantic import BaseModel
from db import get_connection
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------ STATIC FILES ------------------
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

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
        UPDATE questions
        SET is_open=false
        WHERE session_id=%s
          AND is_open=true
          AND auto_close_at IS NOT NULL
          AND auto_close_at < NOW()
        """,
        (session_id,)
    )

    cur.execute(
        """
        SELECT id, text
        FROM questions
        WHERE session_id=%s AND is_open=true
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (session_id,)
    )

    q = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not q:
        return {"id": None}

    return {"id": q[0], "text": q[1]}

# ------------------ SUBMIT ANSWER ------------------
@app.post("/api/answer")
def submit_answer(data: AnswerRequest):
    conn = get_connection()
    cur = conn.cursor()

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

# ------------------ STAR / UNSTAR ANSWER ------------------
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
