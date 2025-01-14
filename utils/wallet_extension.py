import asyncio
from enum import StrEnum

from loguru import logger

from playwright.async_api import Page, TimeoutError, expect

from core.profile import Profile
from utils.enum_constants import Extensions


class WalletExtension:
    @staticmethod
    async def unlock(profile: Profile, page: Page, wallet_name: str):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | WALLET UNLOCK"
        unlocked = False
        try:
            if wallet_name == "RABBY":
                await page.goto(Extensions.RABBY_WALLET)
                await page.locator("[type=password]").fill(profile.wallet_pass)
                await page.locator("[type=submit]").click()
                main_menu_xpath = "//div[contains(@class, 'recent-connections')]/child::div[contains(@class, 'pannel')]"
                await expect(page.locator(main_menu_xpath)).to_be_visible(timeout=10000)
                unlocked = True

            elif wallet_name == "OKX":
                await page.goto(Extensions.OKX_WALLET)
                await page.locator("//input[@data-testid='okd-input']").fill(profile.wallet_pass)
                await page.locator("//button[@data-testid='okd-button']").click()
                await expect(page.locator("//div[@data-testid='okd-tabs-scroll-container']")).to_be_visible(timeout=10000)
                unlocked = True

            elif wallet_name == "PHANTOM":
                await page.goto(Extensions.PHANTOM_WALLET)
                await page.locator("//input[@data-testid='unlock-form-password-input']").fill(profile.wallet_pass)
                await page.locator("//button[@data-testid='unlock-form-submit-button']").click()
                await expect(page.locator("//a[@data-testid='bottom-tab-nav-button-/swap']")).to_be_visible(timeout=10000)
                unlocked = True

        except (AssertionError, TimeoutError) as e:
            logger.error(f"{log_string} | ERROR: {e}")
        except Exception as e:
            logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        return unlocked

    @staticmethod
    async def connect(profile: Profile, page: Page, wallet_name: str, wallet_url: str | StrEnum = 'notification.html'):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | WALLET CONNECT"
        connected = False

        for attempt in range(5):
            wallet_tab = None
            await asyncio.sleep(2)
            all_tabs = page.context.pages

            for tab in all_tabs:
                if wallet_url in tab.url:
                    wallet_tab = tab
                    break

            if not wallet_tab:
                continue

            try:
                if wallet_name == 'RABBY':
                    connect_locator = wallet_tab.get_by_text("Ignore all")
                    if await connect_locator.count() == 1:
                        await connect_locator.click()
                        await asyncio.sleep(3)

                    await wallet_tab.get_by_role(role="button", name="Connect").click()
                    connected = True
                    break

                elif wallet_name == 'OKX':
                    connect_xpath = "//button[@data-testid='okd-button']/descendant::*[contains(text(), 'Connect')]"
                    await wallet_tab.locator(connect_xpath).click()
                    connected = True
                    break

                elif wallet_name == 'PHANTOM':
                    await wallet_tab.locator("//button[@data-testid='primary-button']").click()
                    connected = True
                    break

            except TimeoutError as e:
                logger.error(f"{log_string} | ERROR WHILE CONNECTING: {e}")
            except Exception as e:
                logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        return connected

    @staticmethod
    async def sign(profile: Profile, page: Page, wallet_name: str, wallet_url: str | StrEnum = 'notification.html'):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | WALLET SIGN"
        signed = False

        for attempt in range(5):
            wallet_tab = None
            await asyncio.sleep(2)
            all_tabs = page.context.pages

            for tab in all_tabs:
                if wallet_url in tab.url:
                    wallet_tab = tab
                    break

            if not wallet_tab:
                continue

            try:
                if wallet_name == 'RABBY':
                    await wallet_tab.get_by_text(text="Sign", exact=True).click()
                    await wallet_tab.locator("text=Confirm").click()
                    signed = True
                    break

                elif wallet_name == 'OKX':
                    connect_xpath = "//button[@data-testid='okd-button']/descendant::*[contains(text(), 'Confirm')]"
                    await wallet_tab.locator(connect_xpath).click()
                    signed = True
                    break

                elif wallet_name == 'PHANTOM':
                    await wallet_tab.locator("//button[@data-testid='primary-button']").click()
                    signed = True
                    break

            except TimeoutError as e:
                logger.error(f"{log_string} | ERROR WHILE SIGNING: {e}")
            except Exception as e:
                logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        return signed

    @staticmethod
    async def add(profile: Profile, page: Page, wallet_name: str, wallet_url: str | StrEnum = 'notification.html'):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | WALLET ADD"
        added = False

        for attempt in range(5):
            wallet_tab = None
            await asyncio.sleep(2)
            all_tabs = page.context.pages

            for tab in all_tabs:
                if wallet_url in tab.url:
                    wallet_tab = tab
                    break

            if not wallet_tab:
                continue

            try:
                if wallet_name == 'RABBY':
                    await wallet_tab.get_by_role(role="button", name="Add").click()
                    added = True
                    break

                elif wallet_name == 'OKX':
                    connect_xpath = "//button[@data-testid='okd-button']/descendant::*[contains(text(), 'Approve')]"
                    await wallet_tab.locator(connect_xpath).click()
                    added = True
                    break

                elif wallet_name == 'PHANTOM':
                    pass

            except TimeoutError as e:
                logger.error(f"{log_string} | ERROR WHILE CONNECTING: {e}")
            except Exception as e:
                logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        return added

    @staticmethod
    async def check_stuck_wallet_window(profile: Profile, page: Page):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | CHECK STUCK WALLET WINDOW"
        await asyncio.sleep(2)

        all_pages = page.context.pages
        for tab in all_pages:
            if "notification.html" in tab.url:
                try:
                    await tab.close()
                    logger.debug(f"{log_string} | WALLET WINDOW CLOSED")

                except TimeoutError as e:
                    logger.error(f"{log_string} | ERROR: {e}")
                except Exception as e:
                    logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")
