"""Unit tests for the FastAPI layer in ``api/main.py``.

These exercise the HTTP contract: status codes, response bodies, and the
observable state of the underlying task store after each request.
"""

import pytest

import main


# --------------------------------------------------------------------------
# GET /health
# --------------------------------------------------------------------------

def test_health_check_returns_healthy(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# --------------------------------------------------------------------------
# GET /tasks
# --------------------------------------------------------------------------

def test_get_tasks_returns_all_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "title": "Learn FastAPI", "completed": False},
        {"id": 2, "title": "Understand HTTP", "completed": True},
    ]


def test_get_tasks_returns_empty_list_after_delete_all(client):
    client.delete("/tasks")

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


# --------------------------------------------------------------------------
# GET /tasks/{task_id}
# --------------------------------------------------------------------------

def test_get_task_by_id_returns_task(client):
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False,
    }


def test_get_task_by_id_returns_completed_task(client):
    response = client.get("/tasks/2")

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_get_task_not_found_returns_404(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_task_with_non_integer_id_returns_422(client):
    response = client.get("/tasks/not-a-number")

    assert response.status_code == 422


# --------------------------------------------------------------------------
# POST /tasks
# --------------------------------------------------------------------------

def test_add_task_returns_201_and_message(client):
    response = client.post("/tasks", json={"title": "Buy milk"})

    assert response.status_code == 201
    assert response.json() == {"message": "Task Buy milk added"}


def test_add_task_persists_task(client):
    client.post("/tasks", json={"title": "Buy milk"})

    tasks = client.get("/tasks").json()

    assert len(tasks) == 3
    assert tasks[-1] == {"id": 3, "title": "Buy milk", "completed": False}


def test_add_task_strips_whitespace_from_title(client):
    client.post("/tasks", json={"title": "  Buy milk  "})

    assert client.get("/tasks").json()[-1]["title"] == "Buy milk"


def test_add_task_assigns_incrementing_ids(client):
    client.post("/tasks", json={"title": "First"})
    client.post("/tasks", json={"title": "Second"})

    tasks = client.get("/tasks").json()

    assert [task["id"] for task in tasks] == [1, 2, 3, 4]


def test_add_task_with_blank_title_returns_400(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid title!"}


def test_add_task_with_too_long_title_returns_400(client):
    response = client.post("/tasks", json={"title": "a" * 101})

    assert response.status_code == 400
    assert response.json() == {"detail": "Title is too long!"}


def test_add_task_with_max_length_title_succeeds(client):
    response = client.post("/tasks", json={"title": "a" * 100})

    assert response.status_code == 201


def test_add_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_add_task_rejected_title_is_not_stored(client):
    client.post("/tasks", json={"title": "   "})

    assert len(client.get("/tasks").json()) == 2


# --------------------------------------------------------------------------
# DELETE /tasks/{task_id}
# --------------------------------------------------------------------------

def test_delete_task_by_id_returns_200_and_message(client):
    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {"message": "task_id: 1 has been removed"}


def test_delete_task_by_id_removes_task(client):
    client.delete("/tasks/1")

    tasks = client.get("/tasks").json()

    assert len(tasks) == 1
    assert tasks[0]["id"] == 2


def test_delete_task_not_found_returns_404(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task_not_found_leaves_tasks_untouched(client):
    client.delete("/tasks/999")

    assert len(client.get("/tasks").json()) == 2


# --------------------------------------------------------------------------
# DELETE /tasks  (delete all)
# --------------------------------------------------------------------------

def test_delete_all_tasks_returns_200_and_message(client):
    response = client.delete("/tasks")

    assert response.status_code == 200
    assert response.json() == {"message": "All tasks have been removed"}


def test_delete_all_tasks_empties_the_store(client):
    client.delete("/tasks")

    assert client.get("/tasks").json() == []


def test_delete_all_tasks_on_empty_store_is_ok(client):
    client.delete("/tasks")

    response = client.delete("/tasks")

    assert response.status_code == 200
    assert response.json() == {"message": "All tasks have been removed"}


# --------------------------------------------------------------------------
# PATCH /tasks/{task_id}
# --------------------------------------------------------------------------

def test_complete_task_returns_200_and_message(client):
    response = client.patch("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Task Learn FastAPI completed!"}


def test_complete_task_marks_task_completed(client):
    client.patch("/tasks/1")

    assert client.get("/tasks/1").json()["completed"] is True


def test_complete_already_completed_task_returns_409(client):
    response = client.patch("/tasks/2")

    assert response.status_code == 409
    assert response.json() == {"detail": "Task 2 is already completed"}


def test_complete_task_not_found_returns_404(client):
    response = client.patch("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task id 999 not found"}


def test_complete_task_with_non_integer_id_returns_422(client):
    response = client.patch("/tasks/abc")

    assert response.status_code == 422


# --------------------------------------------------------------------------
# Multi-step flows
# --------------------------------------------------------------------------

def test_task_lifecycle_add_complete_and_delete(client):
    created = client.post("/tasks", json={"title": "Write tests"})
    assert created.status_code == 201

    task_id = client.get("/tasks").json()[-1]["id"]

    completed = client.patch(f"/tasks/{task_id}")
    assert completed.status_code == 200
    assert client.get(f"/tasks/{task_id}").json()["completed"] is True

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 200
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_deleted_task_id_is_not_reused(client):
    client.delete("/tasks/2")

    client.post("/tasks", json={"title": "New task"})

    new_task = client.get("/tasks").json()[-1]
    assert new_task["id"] == 3


@pytest.mark.parametrize(
    "method,path",
    [
        ("get", "/tasks/abc"),
        ("delete", "/tasks/abc"),
        ("patch", "/tasks/abc"),
    ],
)
def test_non_integer_task_id_is_rejected(client, method, path):
    response = getattr(client, method)(path)

    assert response.status_code == 422
