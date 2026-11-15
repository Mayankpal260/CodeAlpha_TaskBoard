# CodeAlpha Task 3 — TaskBoard Project Management Tool

A Django task board demo with projects, task assignments, status/priority, due dates, comments and login.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations board
python manage.py migrate
python manage.py runserver
```
Open http://127.0.0.1:8000/. Register an account, create a project, then add tasks and comments. The app is a local internship demo, not a production team collaboration service.
