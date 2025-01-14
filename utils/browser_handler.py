import asyncio
import json

import requests

from aiohttp import ClientSession, ClientConnectionError, ClientPayloadError, TCPConnector
from asyncio import TimeoutError
from loguru import logger

from core.profile import Profile
from config import ADS_PORT


class BrowserHandler:
    @staticmethod
    async def open(profile: Profile) -> str:
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | BROWSER HANDLER - OPEN"
        connection_url = ''
        url = f"http://local.adspower.net:{ADS_PORT}/api/v1/browser/start?user_id={profile.profile_id}&open_tabs=1&ip_tab=0"
        total_attempts = 50

        try:
            connector = TCPConnector(limit=200)
            async with ClientSession(connector=connector) as session:
                for attempt in range(total_attempts):
                    async with session.get(url) as response:
                        if response.status != 200:
                            logger.error(f"{log_string} | ERROR. STATUS CODE: {response.status}")
                            await asyncio.sleep(5)
                            continue

                        try:
                            response_data = await response.json()

                            if response_data.get('code') == 0 and response_data.get('data', {}).get('ws', {}).get('puppeteer', {}):
                                connection_url = response_data['data']['ws']['puppeteer']
                                return connection_url
                            else:
                                logger.error(f"{log_string} | UNABLE TO GET CONNECTION URL: {response_data}")

                        except json.JSONDecodeError as e:
                            logger.error(f"{log_string} | UNABLE TO DECODE JSON: {e}")

                    await asyncio.sleep(5)

        except (ClientConnectionError, ClientPayloadError, TimeoutError) as e:
            logger.error(f"{log_string} | ERROR: {e}")
        except Exception as e:
            logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        logger.error(f"{log_string} | UNABLE TO LAUNCH A BROWSER")
        return connection_url

    @staticmethod
    async def close(profile: Profile):
        log_string = f"PROFILE {profile.profile_number} ({profile.profile_id}) | BROWSER HANDLER - CLOSE"

        url = f"http://local.adspower.net:{ADS_PORT}/api/v1/browser/stop?user_id={profile.profile_id}"
        total_attempts = 25

        try:
            connector = TCPConnector(limit=200)
            async with ClientSession(connector=connector) as session:
                for attempt in range(total_attempts):
                    async with session.get(url) as response:
                        if response.status != 200:
                            logger.error(f"{log_string} | ERROR. STATUS CODE: {response.status}")
                            await asyncio.sleep(5)
                            continue

                        try:
                            response_data = await response.json()
                            logger.debug(f"{log_string} | response data: {response_data}")

                            if response_data.get('code') == 0:
                                logger.debug(f"{log_string} | BROWSER CLOSED")
                                return

                        except json.JSONDecodeError as e:
                            logger.error(f"{log_string} | UNABLE TO DECODE JSON: {e}")

                    await asyncio.sleep(5)

        except (ClientConnectionError, ClientPayloadError, TimeoutError) as e:
            logger.error(f"{log_string} | ERROR: {e}")
        except Exception as e:
            logger.critical(f"{log_string} | UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

    @staticmethod
    def update_adsbrowser_profiles(i: int, profile_id: str, ads_port: str):
        url = f"http://local.adspower.net:{ads_port}/api/v1/user/update"  # Replace with the actual API endpoint

        fingerprint_config = {
            # "screen_resolution": "1600_900",
            "browser_kernel_config": {
                "version": "128",
                "type": "chrome"
            }
        }

        payload = {
            "user_id": profile_id,
            "open_urls": []
            # "fingerprint_config": fingerprint_config
        }

        # Send the POST request
        response = requests.post(url, json=payload)

        # Print the response (optional)
        print(f"{i}, {profile_id} | status code: {response.status_code} | {response.json()}")
