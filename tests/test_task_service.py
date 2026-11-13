from task_service import TaskService


def test_add_task_basic():
    service = TaskService()
    message = service.add_task("Buy milk")
    assert message == "Task Buy milk added"
    assert service.tasks == [{"id": 1, "title": "Buy milk", "completed": False}]


def test_add_task_strips_title():
    service = TaskService()
    service.add_task("  Buy milk  ")
    assert service.tasks[0]["title"] == "Buy milk"


def test_add_task_empty_title():
    service = TaskService()
    message = service.add_task("   ")
    assert message == "Invalid title!"
    assert service.tasks == []


def test_add_task_too_long():
    service = TaskService()
    message = service.add_task("a" * 101)
    assert message == "Title is too long!"
    assert service.tasks == []


def test_add_task_uid_continues():
    service = TaskService([{"id": 5, "title": "x", "completed": False}])
    service.add_task("y")
    assert service.tasks[-1]["id"] == 6


def test_find_task():
    service = TaskService()
    service.add_task("x")
    assert service.find_task(1) == service.tasks[0]
    assert service.find_task(99) is None


def test_delete_task_by_id():
    service = TaskService()
    service.add_task("x")
    message = service.delete_task(1)
    assert message == "task_id: 1 has been removed"
    assert service.tasks == []


def test_delete_task_not_found():
    service = TaskService()
    service.add_task("x")
    message = service.delete_task(2)
    assert message == "Task not found"
    assert len(service.tasks) == 1


def test_delete_all_tasks():
    service = TaskService()
    service.add_task("x")
    message = service.delete_task(delete_all=True)
    assert message == "All tasks have been removed"
    assert service.tasks == []


def test_complete_task():
    service = TaskService()
    service.add_task("x")
    message = service.complete_task(1)
    assert message == "Task x completed!"
    assert service.tasks[0]["completed"] is True


def test_complete_already_completed():
    service = TaskService()
    service.add_task("x")
    service.complete_task(1)
    message = service.complete_task(1)
    assert message == "Task x is already completed"


def test_complete_not_found():
    service = TaskService()
    message = service.complete_task(1)
    assert message == "Task id 1 not found"
