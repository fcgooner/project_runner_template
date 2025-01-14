import asyncio

from loguru import logger
from playwright.async_api import Page
from random import randint

from core.profile import Profile
from config import CRITICAL_TASKS
from utils.task_handler import update_task_result_in_csv

# TASKS
from .tasks.rekt_login import rekt_login
from .tasks.rekt_stake import rekt_stake
from .tasks.rekt_checkin import rekt_checkin


async def run_rekt(profile: Profile, project: str, tasks: list, page: Page | None = None):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | RUN REKT"
    logger.debug(f"{log_string} | RUN REKT | TASKS LIST: {tasks}")

    for task in tasks:
        logger.info(f"{log_string} | {task} | EXECUTION START")
        task_result = None

        try:
            if task == "REKT LOGIN":
                if profile.get_task_result(task=task) is False:
                    task_result = await rekt_login(profile)

            elif task == "REKT CHECKIN":
                if profile.get_task_result(task=task) is False:
                    task_result = await rekt_checkin(profile)

            elif task == "REKT STAKE":
                if profile.get_task_result(task=task) is False:
                    task_result = await rekt_stake(profile, page)

            else:
                logger.error(f"{log_string} | UNKNOWN TASK: {task}")

            if task_result is True:
                logger.success(f"{log_string} | {task} | RESULT: {task_result}")
            elif task_result is False:
                logger.error(f"{log_string} | {task} | RESULT: {task_result}")

            if task_result is not None and profile.get_task_result(task) != task_result:
                update_task_result_in_csv(profile=profile,
                                          task=task.split()[1],
                                          task_result=task_result,
                                          called_project=project)

                logger.debug(f"{log_string} | {task} | TASK RESULT ADDED TO THE TABLE")

            if task in CRITICAL_TASKS and task_result is False:
                logger.critical(f"{log_string} | {task} | CRITICAL TASK FAILED. STOPPING TASKS EXECUTION")
                break

            logger.info(f"{log_string} | {task} | EXECUTION END")
            await asyncio.sleep(randint(1, 2))


        except Exception as e:
            logger.critical(f"{log_string} | {task} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

    logger.info(f"{log_string} | NO MORE TASKS LEFT")
