# Short Answer ClassPoint

Short Answer ClassPoint provides a live short-answer workflow for teachers and students. Teachers launch questions, review submissions, and view summaries. Students join with a class code, update their profile, and submit answers in real time.

## Apps

### Student Web App
**Location:** `backend/static`  
**Runtime:** FastAPI serving static HTML + student APIs

**Key flows**
* Join a class with a 5-digit code.
* Customize profile details.
* Answer live questions and review submitted responses.

### Teacher Dashboard
**Location:** `teacher/`  
**Runtime:** Flet desktop/web UI

**Key flows**
* Authenticate (login/sign up).
* Configure session options (multiple submissions, anonymization, auto-close).
* Launch questions, monitor live answers, and close submissions.
* Review answers and view post-question summaries.

## Local Development

### Prerequisites
* Python 3.10+
* PostgreSQL running locally
* (Teacher app) `flet` installed

### Database Setup
The backend and teacher apps connect to a local Postgres database using:
* **DB name:** `short_ans_classpoint`
* **User:** `postgres`
* **Password:** `ahmad1807`
* **Host:** `localhost`
* **Port:** `5432`

Create the database if it does not exist:
```bash
createdb short_ans_classpoint
```

### Student App (FastAPI)
```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open:
* Join page: `http://localhost:8000/`
* Profile page: `http://localhost:8000/profile`
* Dashboard: `http://localhost:8000/dashboard`

### Teacher App (Flet)
```bash
pip install flet psycopg2-binary
python teacher/app.py
```

## Suggested Workflow

### Teacher
1. Sign in or create a teacher account.
2. Configure activity options in **Setup**.
3. Start a question in **Dashboard**.
4. Monitor live responses.
5. Close submissions and review summaries.

### Student
1. Enter the class code on the **Join** page.
2. Fill in profile details.
3. Answer live questions in the **Dashboard**.
4. Review submitted answers in **My Answers**.

## Screenshots
The following screenshots are representative snapshots of each page with demo data.

### Student App
![Student join page](docs/screenshots/student-join.svg)
![Student profile page](docs/screenshots/student-profile.svg)
![Student dashboard (active question)](docs/screenshots/student-dashboard-question.svg)
![Student dashboard (my answers)](docs/screenshots/student-dashboard-answers.svg)

### Teacher App
![Teacher login](docs/screenshots/teacher-login.svg)
![Teacher sign up](docs/screenshots/teacher-signup.svg)
![Teacher setup](docs/screenshots/teacher-setup.svg)
![Teacher dashboard](docs/screenshots/teacher-dashboard.svg)
![Teacher live question](docs/screenshots/teacher-live-question.svg)
![Teacher summary view](docs/screenshots/teacher-summary.svg)
![Teacher review answers](docs/screenshots/teacher-review-answers.svg)