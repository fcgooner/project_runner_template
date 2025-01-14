from loguru import logger
from playwright.async_api import Page

from core.profile import Profile


async def lifechanger_login(profile: Profile, page: Page):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | LIFECHANGER LOGIN"
    logger.debug(f"{log_string} | START")

    return False
