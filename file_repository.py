import json
import os
from pathlib import Path


def validate_json(data):
    schema = {
        "id": int,
        "title": str,
        "completed": bool,
    }

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        return False, []

    if len(data) == 0:
        return True, []

    existing_ids = set()

    for task in data:
        if not isinstance(task, dict):
            return False, []

        is_valid = all(
            key in task and isinstance(task[key], expected_type)
            for key, expected_type in schema.items()
        )

        if is_valid:
            if type(task["id"]) is not int or task["id"] <= 0:
                is_valid = False

        if not is_valid:
            return False, []

        if task["id"] in existing_ids:
            return False, []

        if len(task["title"]) > 100:
            return False, []

        existing_ids.add(task["id"])

    return True, data


class FileTaskRepository:
    def __init__(self, filename="tasks.json"):
        self.path = Path(filename).with_suffix(".json")

    @staticmethod
    def validate(data):
        return validate_json(data)

    def load(self):
        if not self.path.exists():
            return f"A file called {self.path} could not be found", None

        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            return f"{self.path} is not valid JSON: {e}", None
        except OSError as e:
            return f"Unable to read file: {e}", None

        is_valid, json_data = validate_json(data)
        if is_valid:
            return f"tasks from {self.path} has been successfully loaded", json_data
        return f"{self.path} does not include valid data", None

    def save(self, tasks):
        try:
            with self.path.open("w", encoding="utf-8") as file:
                json.dump(tasks, file, indent=4)
            return f"Tasks have been saved into {self.path}"
        except OSError as e:
            return f"Unable to save file: {e}"
