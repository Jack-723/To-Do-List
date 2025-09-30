# Minimal Todo API + UI (FastAPI + SQLite)

A simple To-do list application built for my DevOps course.  
Includes a REST API (with Swagger docs) and a lightweight HTML interface.

---

## Features
- CRUD endpoints for todos (`/todos`)
- Persistent storage using SQLite (`todo.db`)
- Interactive API docs at `/docs`
- Simple web UI at `/`

---

## Tech
- Python 3.11+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite database

---

## Quickstart

```bash
# 1. Create virtual environment
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate
# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs
 → Swagger UI (API testing)

http://127.0.0.1:8000/
 → HTML Todo UI

Notes

Made as coursework for DevOps & SDLC pipeline design.

Future improvements: tests, Dockerfile, CI/CD workflow.