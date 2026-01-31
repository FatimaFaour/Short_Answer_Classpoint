from .connect import run_query

def bootstrap_tables():
    # Teachers table
    run_query("""
    CREATE TABLE IF NOT EXISTS teachers (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Sessions table
    run_query("""
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        teacher_id INT REFERENCES teachers(id),
        code TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE
    )
    """)

    # Questions table
    run_query("""
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        session_id INT REFERENCES sessions(id),
        text TEXT NOT NULL,
        is_open BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        auto_close_at TIMESTAMP
    )
    """)

    # Students table
    run_query("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        display_name TEXT NOT NULL
    )
    """)

    # Participants table
    run_query("""
    CREATE TABLE IF NOT EXISTS participants (
        id SERIAL PRIMARY KEY,
        session_id INT REFERENCES sessions(id),
        student_id INT REFERENCES students(id),
        nickname TEXT NOT NULL
    )
    """)

    # Answers table
    run_query("""
    CREATE TABLE IF NOT EXISTS answers (
        id SERIAL PRIMARY KEY,
        question_id INT REFERENCES questions(id),
        student_id INT REFERENCES students(id),
        participant_id INT REFERENCES participants(id),
        answer_text TEXT,
        starred BOOLEAN DEFAULT FALSE,
        submitted_at TIMESTAMP DEFAULT NOW()
    )
    """)

