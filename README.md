
# 📊 PowerPoint Short Answer Add-in

Short Answer ClassPoint is a **PowerPoint VSTO Add-in** paired with a **FastAPI backend** that enables live short-answer questions during presentations. The teacher controls the flow directly from PowerPoint, while students respond through a lightweight web app.
----
**Implemented By:**

Batoul Kanaan -- batoul0120@hotmail.com
Fatima Faour -- Fatiimafr22@gmail.com
----

This README is written as a **simple running guide**, with clear places to add screenshots for:
 
* PowerPoint add-in
* Teacher panel
* Student view
* Student Website view

---
 

## ✨ Features
 
* PowerPoint **Ribbon button** to start a short-answer session
* Automatically **adds a button to the slide**
* Opens a **teacher desktop panel** (login, setup, dashboard, answers, summary, review)
* Starts **Flet App service** for teachers as panel
* Starts **FastAPI backend service** for students
* Student web app with **login, profile, and answering pages**
 

---

## 📁 Project Structure

```
Short_Answer_Classpoint/
│
├── PowerPointVstoAddIn/        # PowerPoint VSTO Add-in (C#)
│   ├── Ribbon.xml
│   ├── Ribbon.cs
│   ├── ThisAddIn.cs
│   └── ...
│
├── backend/                   # FastAPI backend (student web app)
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   └── static/
│       ├── index.html         # Student login
│       ├── profile.html       # Student profile
│       └── dashboard.html     # Student answering page
│
├── teacher/                   # Teacher desktop app
│   ├── app.py
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

### Software

* Windows 10 / 11
* Microsoft PowerPoint (Desktop)
* Visual Studio 2022
* Python 3.10+
* PostgreSQL dB

### Database Setup
The backend and teacher apps connect to a local Postgres database using:
* **DB name:** `short_ans_classpoint`
* **User:** `postgres`
* **Password:** `yourpassword`
* **Host:** `localhost`
* **Port:** `5432`
> Enter your password instead of "yourpassword" 


### Python Packages

 ```bash
pip install -r requirements.txt
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

## 🧩 Running the PowerPoint Add-in

### 1️⃣ Open the VSTO project

* Open `PowerPointVstoAddIn.sln` in **Visual Studio**

### 2️⃣ Build and Run

* Configuration: **Debug**
* Press **F5**

PowerPoint will launch automatically with the add-in loaded.


---![Launch PowerPoint](screenshots/Powerpoint.png)


## 🖱️ Teacher Flow (Desktop App)

> The teacher app runs only when the **VSTO Add-in** is loaded and started from Visual Studio. It opens from the **Teacher Login** entry point.

### Step 1 — Start session

* In PowerPoint, go to **Home → Short Answer**
![PP Screenshot](screenshots/addin.png)
* Click **Start Short Answer**

---

### Step 2 — Slide button added

* A button labeled **“Answer Question”** is added to the current slide
![Ribbon Screenshot](screenshots/ribbon.png)

---

### Step 3 — Teacher login page

* The teacher panel opens on the right
* Click **Teacher Login**
![Login Screenshot](screenshots/TeacherLogin.png)

* You can create your own account
![Signin Screenshot](screenshots/TeacherCreate.png)
**Now Login with your new account**
![LoginNow Screenshot](screenshots/Login.png)
---

### Step 4 — Setup page

  * Configure session settings such as:
  * Multiple submissions
  * Anonymous mode
  * Auto-close timer
![Setup Screenshot](screenshots/TeacherSetup.png)

---

### Step 5 — Quiz page

* Launch a question
![Ques Screenshot](screenshots/Ques.png)

---

### Step 6 — Answers page

* Monitor live answers
* Close submissions when finished
* You can check the correct answer
![Ans Screenshot](screenshots/Answer.png)
* You can check the correct answer
![dash Screenshot](screenshots/dash.png)
#### After Closing Submissions
![ques Screenshot](screenshots/ques2.png)
---

### Step 7 — Summary page

* See aggregated results
* Highlight common answers
![summary Screenshot](screenshots/summary.png)

---

### Step 8 — Review page

* Review individual submissions
![Review Screenshot](screenshots/review.png)

---

## 👩‍🎓 Student Flow (Web App)

### 1. Students open a browser
### 2. Navigate to:

   ```
   http://<teacher-ip>:8000
   ```
   ![Student Page](screenshots/startSt.png)

### 3. Student pages include:

   #### 3.1 **Login Page** – enter class code
   ![Join Screenshot](screenshots/code.png)
   #### 3.2 **Profile Page** – enter name and add profile photo
   ![Profile Screenshot](screenshots/Profile.png)
   #### 3.3 **Answering Page** – receive questions and submit short answers
   * Wait for teacher to send questions
   ![Wait Screenshot](screenshots/wait.png)
   * After asking  write a short answer
   ![Answering Screenshot](screenshots/ans.png)
   * Submit the answer
   ![Submit Screenshot](screenshots/submit.png)
   * In case the question is timeout:
   ![Close Screenshot](screenshots/closed.png)

---

## 🔒 Notes

* The teacher desktop app and student web app **run only when the VSTO add-in is started**.
* PowerPoint must be started via **Visual Studio** when debugging.
* Backend services run locally by default.
* Ports can be changed in code if needed.

---


## 👨‍🏫 Academic Context

This project demonstrates:

* Desktop application extensibility (VSTO)
* Client-server integration
* Event-driven UI design
* Educational technology workflows


---
