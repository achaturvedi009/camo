import asyncio
import os
from camoufox.async_api import AsyncCamoufox

async def main():
    os.makedirs("test_profile", exist_ok=True)
    async with AsyncCamoufox(headless=True) as browser:
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())

asyncio.run(main())