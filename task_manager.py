from task_service import TaskService
from file_repository import FileTaskRepository

TASKS_FILE = "tasks.json"

def print_tasks(tasks):
    if len(tasks) == 0:
        print("No tasks have been added yet!")
    else:
        for task in tasks:
            print("ID:", task["id"])
            print("Title:", task["title"])
            if task["completed"]:
                print("Status: Completed")
            else:
                print("Status: Incomplete")


def main():
    repository = FileTaskRepository(TASKS_FILE)
    init_response, task_list = repository.load()
    print(f"{init_response} \n")

    if task_list is not None:
        service = TaskService(task_list)
    else:
        service = TaskService()

    while True:
        print("\n")
        print("==============================")
        print("         TASK MANAGER         ")
        print("==============================")
        print("\n")
        print("1. Add task")
        print("2. Delete task(s)")
        print("3. List Tasks")
        print("4. Complete Task")
        print("5. Load Saved Tasks")
        print("6. Save to File")
        print("7. Exit \n")

        menu_input = input("Select an option: ").strip()

        match menu_input:
            case "1":
                task_title = input("Input task title: ")
                print(service.add_task(task_title))

            case "2":
                option = input("Delete all tasks? (y/n): ")
                if option == "n":
                    task_id = input("Input task id for deletion: ")
                    try:
                        task_id = int(task_id)
                        print(service.delete_task(task_id))
                    except ValueError:
                        print("Invalid id")
                elif option == "y":
                    print(service.delete_task(delete_all=True))
                else:
                    print("Invalid Response!")

            case "3":
                print_tasks(service.tasks)

            case "4":
                task_id = input("Enter task id: ")
                try:
                    task_id = int(task_id)
                    print(service.complete_task(task_id))
                except ValueError:
                    print("Invalid id")

            case "5":
                option = input("This will delete unsaved changes (y/n): ").strip().lower()
                if option == "y":
                    response, task_list = repository.load()
                    print(response)
                    if task_list is not None:
                        service = TaskService(task_list)
                        print_tasks(service.tasks)
                else:
                    print("Invalid Response!")

            case "6":
                print(repository.save(service.tasks))

            case "7":
                print(repository.save(service.tasks))
                print("Goodbye!")
                break

            case _:
                print("Invalid input")


main()
