## ##

def task_schema(task) -> dict:
    return {
        "id": str(task["_id"]),  # Convierte ObjectId a cadena
        "title": task["title"],
        "description": task.get("description"),
        "completed": task.get("completed", False),
    }


def tasks_schema(tasks)->list:
    return [task_schema(task)for task in tasks]