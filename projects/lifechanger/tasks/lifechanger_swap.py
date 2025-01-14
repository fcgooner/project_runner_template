from loguru import logger

from core.profile import Profile


async def lifechanger_swap(profile: Profile):
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | LIFECHANGER SWAP"
    logger.debug(f"{log_string} | START")

    return True
