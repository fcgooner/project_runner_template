import asyncio
import socket
from datetime import date, datetime

from imap_tools import MailBox, AND
from imap_tools.errors import MailboxLoginError
from loguru import logger

from core.profile import Profile


async def get_code(profile: Profile, subject: str, current_time: datetime):
    """
    Args:
        current_time (datetime): The current timestamp.
            Use datetime.now(timezone.utc).replace(microsecond=0)

    Returns:
        int: A verification code if found or 0 (zero).
    """
    log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | EMAIL PARSER"

    imap_server = None
    imap_servers = {
        'icloud.com': 'imap.mail.me.com',
        'gmail.com': 'imap.gmail.com',
        'outlook.com': 'outlook.office365.com',
    }

    current_date = date.today()
    email_folders = []

    # IF ICLOUD - FOR SUB-ADDRESSES USE MAIN EMAIL AS LOGIN
    if 'icloud' in profile.email_address:
        username = 'main_account@icloud.com'
    else:
        username = profile.email_address

    for domain in imap_servers:
        if domain in username:
            imap_server = imap_servers[domain]
            break

    if imap_server is None:
        return 0

    try:
        with MailBox(imap_server).login(username, profile.email_pass, initial_folder='Inbox') as mailbox:
            logger.debug(f"{log_string} | SEARCHING EMAIL...")

            # # GET FOLDERS LIST
            # for folder in mailbox.folder.list():
            #     email_folders.append(folder.name)

            for attempt in range(10):
                for msg in mailbox.fetch(AND(subject=subject, date=current_date, to=profile.email_address)):
                    if msg.date > current_time:
                        email_text = msg.text.split()

                        for word in email_text:
                            if len(word) == 6 and word.isdigit():
                                return word

                if attempt == 9:
                    logger.error(f"{log_string} | EMAIL WITH CODE NOT FOUND")

                logger.debug(f"{log_string} | NO EXPECTED EMAIL. RETRY IN 10 SECONDS...")
                await asyncio.sleep(10)

    except MailboxLoginError as e:
        logger.error(f"{log_string} | LOGIN ERROR: {e}")
    except socket.error as e:
        logger.error(f"{log_string} | SOCKET ERROR: {e}")
    except Exception as e:
        logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

    return 0