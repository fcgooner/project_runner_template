from loguru import logger

from core.profile import Profile


async def rekt_checkin(profile: Profile):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | REKT CHECKIN"
    logger.debug(f"{log_string} | START")

    return True
