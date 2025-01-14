import random
import asyncio

from loguru import logger
from playwright.async_api import async_playwright, Page

from core.profile import Profile
from config import BROWSERLESS_TASKS, PROJECTS, WALLETS_TO_UNLOCK
from utils.browser_handler import BrowserHandler
from utils.task_handler import get_not_executed_tasks_for_profile
from utils.wallet_extension import WalletExtension

# PROJECTS
from projects.lifechanger import lifechanger
from projects.rekt import rekt


async def project_runner(profile: Profile, project_tasks: dict, page: Page | None = None):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | PROJECT RUNNER"

    for project in project_tasks:
        tasks = project_tasks[project]

        # if not tasks:
        #     continue

        try:
            if project == 'LIFECHANGER':
                await lifechanger.run_lifechanger(profile=profile, project=project, tasks=tasks, page=page)

            elif project == 'REKT':
                await rekt.run_rekt(profile=profile, project=project, tasks=tasks, page=page)

            else:
                logger.error(f"{log_string} | UNKNOWN PROJECT: {project}")

        except Exception as e:
            logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

    logger.info(f"{log_string} | EXIT")


async def project_handler(profile: Profile, semaphore: asyncio.Semaphore):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | PROJECT HANDLER"

    async with semaphore:
        try:
            project_list = PROJECTS.copy()
            random.shuffle(project_list)

            browser_required = False
            project_tasks = {}
            for project in project_list:
                task_list = get_not_executed_tasks_for_profile(profile, project)
                if not task_list:
                    continue
                project_tasks[project] = task_list

                if not browser_required:
                    browser_required = any(task not in BROWSERLESS_TASKS for task in task_list)

            if not project_tasks:
                logger.warning(f"{log_string} | NO TASKS TO EXECUTE: {project_tasks}")
                return

            logger.info(f"{log_string} | START")

            if not browser_required:
                await project_runner(profile, project_tasks)

            else:
                connect_url = await BrowserHandler.open(profile)
                if not connect_url:
                    return

                async with async_playwright() as playwright:
                    browser = await playwright.chromium.connect_over_cdp(connect_url)
                    context = browser.contexts[0]
                    page = await context.new_page()
                    await page.set_viewport_size({"width": 1600, "height": 900})

                    for wallet in WALLETS_TO_UNLOCK:
                        await WalletExtension.unlock(profile, page, wallet)

                    await project_runner(profile, project_tasks, page)

                await BrowserHandler.close(profile)

        except Exception as e:
            logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        logger.info(f"{log_string} | EXIT")
