class TaskService:
    def __init__(self, tasks=None):
        self.tasks = tasks or []
        self._next_id = max((t["id"] for t in self.tasks), default=0) + 1

    # Function which returns a task with task_id from the task list
    def find_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    # Function to add a task to the task list
    def add_task(self, task_title):
        if task_title.strip() == "":
            return "Invalid title!"
        
        # Create task obj
        if len(task_title) > 100:
            return "Title is too long!"
        
        task = {
            "id": self._next_id,
            "title": task_title.strip(),
            "completed" : False  
        }
    
        self._next_id += 1
        self.tasks.append(task)
        return f'Task {task["title"]} added'

    # Function to delete tasks, handles by id or all
    def delete_task(self, task_id=None, delete_all=False):
        if delete_all:
            self.tasks = []
            return "All tasks have been removed"
        task = self.find_task(task_id)
        if task is None:
            return "Task not found"
        self.tasks.remove(task)
        return f'task_id: {task_id} has been removed'

    # Marks a task with task_id as completed
    def complete_task(self, task_id):
        task = self.find_task(task_id)

        if task is None:
            return f'Task id {task_id} not found'
        
        if task["completed"]:
            return f'Task {task["title"]} is already completed'
        
        task["completed"] = True
        return f'Task {task["title"]} completed!'