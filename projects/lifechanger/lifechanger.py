import asyncio

from loguru import logger
from playwright.async_api import Page
import random

from config import CRITICAL_TASKS
from core.profile import Profile
from utils.task_handler import update_task_result_in_csv

# TASKS
from .tasks.lifechanger_login import lifechanger_login
from .tasks.lifechanger_vote import lifechanger_vote
from .tasks.lifechanger_faucet import lifechanger_faucet
from .tasks.lifechanger_swap import lifechanger_swap


async def run_lifechanger(profile: Profile, project: str, tasks: list, page: Page | None = None):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | RUN LIFECHANGER"
    logger.debug(f"{log_string} | TASK LIST: {tasks}")
    for task in tasks:
        logger.info(f"{log_string} | {task} | EXECUTION START")
        task_result = None

        try:
            if task == "LIFECHANGER LOGIN":
                if profile.get_task_result(task) is False:
                    task_result = await lifechanger_login(profile, page)

            elif task == "LIFECHANGER VOTE":
                if profile.get_task_result(task) is False:
                    task_result = await lifechanger_vote(profile, page)

            elif task == "LIFECHANGER FAUCET":
                if profile.get_task_result(task) is False:
                    task_result = await lifechanger_faucet(profile, page)

            elif task == "LIFECHANGER SWAP":
                if profile.get_task_result(task) is False:
                    task_result = await lifechanger_swap(profile)

            else:
                logger.error(f"{log_string} | UNKNOWN TASK: {task}")
                continue

            if task_result is True:
                logger.success(f"{log_string} | {task} | RESULT: {task_result}")
            else:
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
            await asyncio.sleep(random.randint(1, 2))

        except Exception as e:
            logger.critical(f"{log_string} | {task} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

    logger.info(f"{log_string} | LIFECHANGER | NO MORE TASKS LEFT")
