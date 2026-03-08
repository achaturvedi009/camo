import asyncio
from camoufox.async_api import AsyncCamoufox

async def main():
    try:
        async with AsyncCamoufox(headless=True, os="windows") as browser:
            page = await browser.new_page()
            await page.goto("https://bot.sannysoft.com/")
            await page.screenshot(path="sannysoft.png")
            print("OK")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
