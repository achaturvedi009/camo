import asyncio
import os
from camoufox.async_api import AsyncCamoufox

async def main():
    os.makedirs("test_profile", exist_ok=True)
    async with AsyncCamoufox(headless=True, user_data_dir="test_profile") as browser:
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())

asyncio.run(main())
