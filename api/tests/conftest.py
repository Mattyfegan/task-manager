"""Shared fixtures for the API test suite.

Two things need care here:

1. ``api/main.py`` imports ``task_service`` from the repository root, so both the
   ``api`` directory and the repository root must be importable. ``pytest.ini``
   sets ``pythonpath = .. .`` for this; the block below is a fallback so the
   suite still runs if it is invoked with a different config.
2. ``api/main.py`` holds a module-level ``TaskService`` singleton. Every request
   mutates that one instance, so tests share it and each test starts from a
   known state via the ``reset_tasks`` fixture.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

API_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = API_DIR.parent

for _path in (str(API_DIR), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import main  # noqa: E402  (import must follow the sys.path setup above)


#: The task store as it is seeded in ``api/main.py``.
SEED_TASKS = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Understand HTTP", "completed": True},
]


@pytest.fixture
def client():
    """A ``TestClient`` bound to the app."""
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_tasks():
    """Restore the task store to its seeded state around each test.

    Without this, mutations performed by one test leak into the next and the
    suite becomes order-dependent.
    """
    def _seed():
        main.tasks.tasks = [dict(task) for task in SEED_TASKS]
        main.tasks._next_id = 3

    _seed()
    yield
    _seed()
