import random

from loguru import logger

from core.profile import Profile


async def rekt_login(profile: Profile):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | REKT LOGIN"
    logger.debug(f"{log_string} | START")

    return random.choice([True, False, False])
