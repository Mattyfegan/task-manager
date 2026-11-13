import json
import os
from pathlib import Path

from file_repository import FileTaskRepository, validate_json


def test_path_adds_suffix():
    assert FileTaskRepository("tasks").path == Path("tasks.json")
    assert FileTaskRepository("tasks.json").path == Path("tasks.json")


def test_validate_json_valid_list():
    data = [{"id": 1, "title": "a", "completed": False}]
    is_valid, result = validate_json(data)
    assert is_valid is True
    assert result == data


def test_validate_json_empty_list():
    is_valid, result = validate_json([])
    assert is_valid is True
    assert result == []


def test_validate_json_single_dict():
    data = {"id": 1, "title": "a", "completed": False}
    is_valid, result = validate_json(data)
    assert is_valid is True
    assert result == [data]


def test_validate_json_invalid_type():
    is_valid, result = validate_json("not a list")
    assert is_valid is False
    assert result == []


def test_validate_json_duplicate_id():
    data = [
        {"id": 1, "title": "a", "completed": False},
        {"id": 1, "title": "b", "completed": False},
    ]
    is_valid, result = validate_json(data)
    assert is_valid is False
    assert result == []


def test_validate_json_title_too_long():
    data = [{"id": 1, "title": "a" * 101, "completed": False}]
    is_valid, result = validate_json(data)
    assert is_valid is False
    assert result == []


def test_validate_json_bool_id_rejected():
    data = [{"id": True, "title": "a", "completed": False}]
    is_valid, result = validate_json(data)
    assert is_valid is False
    assert result == []


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    repository = FileTaskRepository("tasks")
    tasks = [{"id": 1, "title": "a", "completed": False}]
    message = repository.save(tasks)
    assert "saved" in message.lower()
    assert (tmp_path / "tasks.json").exists()

    message, loaded = repository.load()
    assert "successfully loaded" in message
    assert loaded == tasks


def test_load_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    repository = FileTaskRepository("nope")
    message, loaded = repository.load()
    assert "could not be found" in message
    assert loaded is None


def test_load_invalid_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
    repository = FileTaskRepository("bad")
    message, loaded = repository.load()
    assert "not valid JSON" in message
    assert loaded is None


def test_load_invalid_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "bad.json").write_text(
        json.dumps([{"id": 1, "title": "a" * 101, "completed": False}]),
        encoding="utf-8",
    )
    repository = FileTaskRepository("bad")
    message, loaded = repository.load()
    assert "does not include valid data" in message
    assert loaded is None
