# Task Manager

A small command-line task manager built in Python for learning backend fundamentals. 

## Project layout

```
task_manager.py      # CLI entry point
task_service.py     # Task business logic (TaskService)
file_repository.py  # JSON storage (FileTaskRepository)
tests/              # pytest test suite (CLI + service layer)
api/                # HTTP API layer (FastAPI)
api/tests/          # pytest test suite (API layer)
db/                 # (planned) database layer
```

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run

```bash
python task_manager.py
```

Tasks are saved to `tasks.json` in the working directory (ignored by git).

### Run the API

```bash
pip install -r api/requirements.txt

# from inside api/
cd api
uvicorn main:app --reload

# or from the repository root
uvicorn api.main:app --reload
```

The API is then available at <http://127.0.0.1:8000>, with interactive docs at
`/docs`.

## Tests

```bash
# CLI / service layer
pytest

# API layer
cd api
pytest
```

The API suite uses `fastapi.testclient.TestClient`, so no server needs to be
running. Tests run against the app's in-memory task store, which is reset
between tests to keep them order-independent.

## Roadmap

- Add pytest coverage for helpers
- Add a proper HTTP API
- Add a database backend
