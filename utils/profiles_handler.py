from loguru import logger

from core.profile import Profile
from config import PROJECTS
from utils.enum_constants import Colors
from utils.file_handler import FileHandler


def initialize_profiles(all_tasks: list[str]) -> (list[Profile], list[Profile]):
    profiles = FileHandler.load_profiles_from_csv('core/profile_database.csv')

    # FILL PROFILES WITH DATA FROM TASK TABLES
    for profile in profiles:
        for project in PROJECTS:
            csv_file = FileHandler.get_project_csv_path(project)

            FileHandler.load_task_results_from_csv(profile, csv_file, project, all_tasks)

    return profiles


def print_summary(original_profile_list: list, all_tasks: list[str]):
    profiles_and_tasks = {}
    task_summary = {}
    bold = "\033[1m"

    for project in PROJECTS:
        csv_filepath = f"projects/{project.lower()}/project_data/tasks_data.csv"
        profiles_and_tasks[project] = FileHandler.get_profile_ids(csv_filepath)

    final_msg = f"\n{Colors.BACKGROUND_WHITE}{Colors.BLACK}{bold} RESULT SUMMARY: {Colors.RESET}\n"

    for profile in original_profile_list:
        profile.print_task_results(all_tasks)

        for project, tasks in profile.task_results.items():
            if project not in task_summary:
                task_summary[project] = {}

            for task_name, result in tasks.items():
                if task_name not in task_summary[project]:
                    task_summary[project][task_name] = 0
                if result:
                    task_summary[project][task_name] += 1

    max_task_name_length = max(
        (len(task_name) for tasks in task_summary.values() for task_name in tasks), default=0
    )
    max_ratio_length = max(
        (len(f"{success_count}/{len(profiles_and_tasks[project])}")
         for project, tasks in task_summary.items() for success_count in tasks.values()), default=0
    )

    if task_summary:
        for project, tasks in task_summary.items():
            project_profiles = len(profiles_and_tasks[project]) \
                if len(profiles_and_tasks[project]) <= len(original_profile_list) else len(original_profile_list)

            final_msg += f"  {bold}{Colors.BLUE}{project}{Colors.RESET}\n"
            for task_name, success_count in tasks.items():
                ratio = f"{success_count}/{project_profiles}"
                final_msg += (
                    f"    {Colors.YELLOW}{bold}{task_name.ljust(max_task_name_length)}: {ratio.rjust(max_ratio_length)}{Colors.RESET}\n"
                )

    logger.opt(raw=True).info(final_msg)

