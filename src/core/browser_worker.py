import asyncio
import sys
import json
import traceback
import signal
import os
import importlib.util

async def main(profile_json: str):
    profile = json.loads(profile_json)

    if "camoufox_lib_path" in profile and profile["camoufox_lib_path"]:
        sys.path.insert(0, profile["camoufox_lib_path"])

    from camoufox.async_api import AsyncCamoufox
    from src.runtime_spoofer.core.runtime_injector import runtime_injector

    headless_env = os.environ.get("HEADLESS", "false").lower() == "true"

    launch_options = {
        "headless": headless_env or False,
        "persistent_context": True,
        "user_data_dir": profile["user_data_dir"],
    }

    if "DISPLAY" not in os.environ and not headless_env:
        launch_options["headless"] = "virtual"

    fp_data = profile.get("fingerprint")
    if fp_data:
        # Fallback to internal fingerprint logic on Camoufox via OS passing for initial binary patches
        # Or you could let Camoufox handle things internally. But we are also adding JS injection.
        launch_options["os"] = profile.get("os", "windows")
    else:
        launch_options["os"] = profile.get("os", "windows")

    if "proxy" in profile and profile["proxy"]:
        proxy_conf = profile["proxy"]
        server = f"{proxy_conf['type']}://{proxy_conf['host']}:{proxy_conf['port']}"
        launch_options["proxy"] = {"server": server}
        if proxy_conf.get("username") and proxy_conf.get("password"):
            launch_options["proxy"]["username"] = proxy_conf["username"]
            launch_options["proxy"]["password"] = proxy_conf["password"]

    try:
        async with AsyncCamoufox(**launch_options) as browser:
            # Inject Runtime Spoofer using add_init_script for all pages in context
            if fp_data:
                init_script = runtime_injector.build_init_script(fp_data)
                await browser.add_init_script(init_script)

            pages = browser.pages
            if not pages:
                page = await browser.new_page()
            else:
                page = pages[0]

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
