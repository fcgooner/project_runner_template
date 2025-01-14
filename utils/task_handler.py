import csv

from loguru import logger
from random import shuffle, randint

from core.profile import Profile
from config import PROJECTS, PROJECT_TASKS
from utils.file_handler import FileHandler


def update_task_result_in_csv(profile: Profile, task: str, task_result: bool, called_project: str) -> None:
    profile.set_task_result(called_project, task, task_result)

    for project in PROJECTS:
        filepath = FileHandler.get_project_csv_path(project)

        if called_project.lower() in filepath:
            task_name = task.split()[-1]
            update_task_csv(
                csv_filepath=filepath,
                profile_id=profile.profile_id,
                column_name=task_name.upper(),
                new_value=str(task_result)
            )
            logger.debug(
                f"PROFILE {profile.profile_number} ({profile.profile_id}) | RESULT OF '{task}' RECORDED TO CSV-TABLE")
            return


def update_task_csv(csv_filepath, profile_id=None, column_name=None, new_value=None):
    updated_rows = []

    with open(csv_filepath, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)

        for row in csvreader:
            updated_row = {'PROFILE_ID': row['PROFILE_ID']}
            for key in row.keys():
                if key == 'PROFILE_ID':
                    continue

                if profile_id and column_name and new_value is not None:
                    if row['PROFILE_ID'] == profile_id and key == column_name:
                        updated_row[key] = new_value
                    else:
                        updated_row[key] = row[key]
                else:
                    updated_row[key] = 'False'

            updated_rows.append(updated_row)

    # WRITE UPDATED ROWS
    with open(csv_filepath, mode='w', newline='') as csvfile:
        fieldnames = updated_rows[0].keys()
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        csvwriter.writeheader()
        csvwriter.writerows(updated_rows)


def get_not_executed_tasks_for_profile(profile: Profile, project: str) -> list[str]:
    project_core_tasks = []
    project_optional_tasks = []
    project_group_tasks = []

    for task in PROJECT_TASKS[project.upper()]['CORE']:
        project_core_tasks.append(task)

    for task in PROJECT_TASKS[project.upper()]['OPTIONAL']:
        project_optional_tasks.append(task)

    for task in PROJECT_TASKS[project.upper()]['GROUP']:
        project_group_tasks.append(task)

    shuffle(project_optional_tasks)

    random_index = randint(0, len(project_optional_tasks))

    project_optional_tasks = (
            project_optional_tasks[:random_index] +
            project_group_tasks +
            project_optional_tasks[random_index:]
    )

    tasks = []
    for task in (project_core_tasks + project_optional_tasks):
        if profile.get_task_result(task) is False:
            tasks.append(task)

    return tasks
