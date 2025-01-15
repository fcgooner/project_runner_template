import asyncio
import requests
from playwright.async_api import async_playwright

async def launch_profile():
    port = 00000
    profile_id = 'grt56jd'

    #open_url = f'http://local.adspower.net:{port}/api/v1/browser/start?user_id={profile_id}&open_tabs=1&ip_tab=0&launch_args=["--headless"]'
    open_url = f'http://local.adspower.net:{port}/api/v1/browser/start?user_id={profile_id}&open_tabs=1'
    close_url = f"http://local.adspower.net:{port}/api/v1/browser/stop?user_id={profile_id}"

    # payload = {
    #     "launch_args": ["--headless=new"]
    # }

    response = requests.get(open_url)
    response_data = response.json()
    print(f"response data: {response_data}")
    print(f"url: {response_data['data']['ws']['puppeteer']}")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(response_data['data']['ws']['puppeteer'])
        context = browser.contexts[0]
        page = await context.new_page()

        try:
            await page.goto('https://google.com')
        except Exception as e:
            print(f"UNHANDLED ERROR: {type(e).__name__}, details: {e.__dict__}")

        # YOUR CODE

    requests.get(close_url)

asyncio.run(launch_profile())
