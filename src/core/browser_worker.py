import asyncio
import sys
import json
import traceback
import signal
from camoufox.async_api import AsyncCamoufox
import os

async def main(profile_json: str):
    profile = json.loads(profile_json)

    launch_options = {
        "headless": False,
        "persistent_context": True,
        "user_data_dir": profile["user_data_dir"],
        "os": profile["os"],
    }

    if "proxy" in profile and profile["proxy"]:
        proxy_conf = profile["proxy"]
        server = f"{proxy_conf['type']}://{proxy_conf['host']}:{proxy_conf['port']}"
        launch_options["proxy"] = {"server": server}
        if proxy_conf.get("username") and proxy_conf.get("password"):
            launch_options["proxy"]["username"] = proxy_conf["username"]
            launch_options["proxy"]["password"] = proxy_conf["password"]

    try:
        async with AsyncCamoufox(**launch_options) as browser:
            pages = browser.pages
            if not pages:
                page = await browser.new_page()
            else:
                page = pages[0]

            # Keep loop alive until all pages are closed
            while True:
                if not browser.pages:
                    break
                await asyncio.sleep(1)

            print("All pages closed. Exiting.")

    except Exception as e:
        print(f"Error launching browser: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python browser_worker.py '<profile_json>'")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    profile_data = sys.argv[1]
    asyncio.run(main(profile_data))
