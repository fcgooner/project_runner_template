import asyncio
import random
import sys

from datetime import datetime

from loguru import logger

from config import FRESH_RUN, MAX_CYCLES, PROJECTS, CONCURRENT_PROFILES, LOG_LEVEL_CONSOLE, LOG_LEVEL_FILE, LOG_TO_FILE
from utils.enum_constants import Colors
from project_handler import project_handler
from utils.file_handler import FileHandler
from utils.profiles_handler import initialize_profiles, print_summary
from utils.task_handler import update_task_csv
from utils.utils import get_all_tasks


async def main():
    if not FRESH_RUN:
        logger.critical(f"MAIN | THIS IS NOT A FRESH RUN!")

    # RESET TASK RESULTS BEFORE RUN
    else:
        for project in PROJECTS:
            filepath = FileHandler.get_project_csv_path(project)
            update_task_csv(csv_filepath=filepath)
        logger.info("MAIN | TASK CSV-TABLES ARE RESET")

    # GET TASK AND PROFILE LISTS
    all_tasks = get_all_tasks()
    original_profile_list = initialize_profiles(all_tasks)
    semaphore = asyncio.Semaphore(CONCURRENT_PROFILES)

    # #UPDATE ADS BROWSER PROFILES
    # for num, profile in enumerate(original_profile_list):
    #     BrowserHandler.update_adsbrowser_profiles(num, profile.profile_id, ADS_PORT)
    #     time.sleep(5)
    #
    # exit()

    for cycle in range(1, MAX_CYCLES + 1):
        if cycle > 1:
            sleep_time = random.randint(30, 60)
            logger.info(f"MAIN | SLEEPING {sleep_time} SECONDS BEFORE NEXT CYCLE")
            await asyncio.sleep(sleep_time)

        all_profiles = original_profile_list.copy()
        random.shuffle(all_profiles)
        logger.info(f"MAIN | START OF CYCLE {cycle}/{MAX_CYCLES}")

        try:
            async_tasks = [asyncio.create_task(project_handler(profile, semaphore)) for profile in all_profiles]
            await asyncio.wait(async_tasks)

        except Exception as e:
            logger.critical(f"MAIN | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        logger.info(f"MAIN | END OF CYCLE {cycle}/{MAX_CYCLES}")

        print_summary(original_profile_list, all_tasks)

    if not FRESH_RUN:
        logger.critical(f"MAIN | THIS WAS NOT A FRESH RUN!")


if __name__ == "__main__":
    logger.remove()
    logger.level("DEBUG", color=Colors.DARK_GRAY)

    logger.add(
        sink=sys.stdout,
        level=LOG_LEVEL_CONSOLE,
        colorize=True
    )

    if LOG_TO_FILE:
        logger.add(
            sink=f"logs/logfile_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
            rotation="00:00",
            retention="1 day",
            level=LOG_LEVEL_FILE
        )

    asyncio.run(main())
