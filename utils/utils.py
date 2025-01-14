from config import PROJECT_TASKS


def get_all_tasks() -> list[str]:
    all_tasks = []

    for project in PROJECT_TASKS:
        for task in PROJECT_TASKS[project]['CORE']:
            all_tasks.append(task)

        for task in PROJECT_TASKS[project]['OPTIONAL']:
            all_tasks.append(task)

        for task in PROJECT_TASKS[project]['GROUP']:
            all_tasks.append(task)

    return all_tasks
