# Task Manager

A small command-line task manager built in Python for learning backend fundamentals. 

## Project layout

```
task_manager.py      # CLI entry point
task_service.py     # Task business logic (TaskService)
file_repository.py  # JSON storage (FileTaskRepository)
tests/              # pytest test suite
api/                # (planned) HTTP API layer
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

## Tests

```bash
pytest
```

## Roadmap

- Add pytest coverage for helpers
- Add a proper HTTP API
- Add a database backend
