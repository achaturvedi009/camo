from camoufox.async_api import AsyncCamoufox
import asyncio

async def test():
    # Let's try to set explicit parameters instead of passing fingerprint object
    try:
        async with AsyncCamoufox(headless=True, os="windows") as browser:
            page = await browser.new_page()
            print("Title:", await page.title())
    except Exception as e:
        print("Launch failed:", e)

asyncio.run(test())
