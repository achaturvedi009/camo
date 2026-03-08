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
    from src.chrome_emulation.integration.runtime_loader import get_chrome_emulation_bundle
    from src.permissions_spoofer.core.permissions_injector import permissions_injector
    from src.permissions_spoofer.integration.fingerprint_permission_mapper import generate_permission_rules
    from src.canvas_spoofer.core.canvas_injector import canvas_injector
    from src.canvas_spoofer.integration.fingerprint_canvas_adapter import integrate_canvas_seed
    from src.webgl_spoofer.core.webgl_injector import webgl_injector
    from src.webgl_spoofer.integration.fingerprint_webgl_adapter import integrate_webgl_seed
    from src.audio_spoofer.core.audio_injector import audio_injector
    from src.audio_spoofer.integration.fingerprint_audio_adapter import integrate_audio_seed
    from src.font_spoofer.core.font_injector import font_injector
    from src.font_spoofer.integration.fingerprint_font_adapter import integrate_font_seed
    from src.webrtc_protector.core.webrtc_injector import webrtc_injector
    from src.webrtc_protector.integration.fingerprint_webrtc_adapter import integrate_webrtc_config
    from src.screen_spoofer.core.screen_injector import screen_injector
    from src.screen_spoofer.integration.fingerprint_display_adapter import integrate_display_config

    headless_env = os.environ.get("HEADLESS", "false").lower() == "true"

    launch_options = {
        "headless": headless_env or False,
        "persistent_context": True,
        "user_data_dir": profile["user_data_dir"],
    }

    if "DISPLAY" not in os.environ and not headless_env:
        launch_options["headless"] = "virtual"

    os_type = profile.get("os", "windows")
    fp_data = profile.get("fingerprint")
    if fp_data:
        launch_options["os"] = os_type
    else:
        launch_options["os"] = os_type

    proxy_host = None
    if "proxy" in profile and profile["proxy"]:
        proxy_conf = profile["proxy"]
        proxy_host = proxy_conf.get('host')
        server = f"{proxy_conf['type']}://{proxy_conf['host']}:{proxy_conf['port']}"
        launch_options["proxy"] = {"server": server}
        if proxy_conf.get("username") and proxy_conf.get("password"):
            launch_options["proxy"]["username"] = proxy_conf["username"]
            launch_options["proxy"]["password"] = proxy_conf["password"]

    try:
        async with AsyncCamoufox(**launch_options) as browser:
            if fp_data:
                profile_id = profile.get("id", "default")

                # Assign dynamic properties derived from main FP hash
                fp_data["permissions"] = generate_permission_rules(fp_data)
                fp_data = integrate_canvas_seed(fp_data, profile_id)
                fp_data = integrate_webgl_seed(fp_data)
                fp_data = integrate_audio_seed(fp_data, profile_id)
                fp_data = integrate_font_seed(fp_data, os_type)
                fp_data = integrate_webrtc_config(fp_data, active_proxy_host=proxy_host)
                fp_data = integrate_display_config(fp_data)

                # 1. Base Fingerprint Variables & General Spoofing
                init_script = runtime_injector.build_init_script(fp_data)

                # 2. Permissions Emulation
                init_script += "\n\n" + permissions_injector.get_injection_script()

                # 3. Canvas Emulation
                init_script += "\n\n" + canvas_injector.get_injection_script()

                # 4. WebGL Emulation
                init_script += "\n\n" + webgl_injector.get_injection_script()

                # 5. Audio Context Emulation
                init_script += "\n\n" + audio_injector.get_injection_script()

                # 6. Font Emulation
                init_script += "\n\n" + font_injector.get_injection_script()

                # 7. WebRTC Protector
                init_script += "\n\n" + webrtc_injector.get_injection_script()

                # 8. Screen Spoofer
                init_script += "\n\n" + screen_injector.get_injection_script()

                # 9. Chrome Specific Environment Emulation (if it's a chrome profile)
                is_chrome = "Chrome" in fp_data.get("userAgent", "") or "Chrome" in fp_data.get("navigator", {}).get("userAgent", "")
                if is_chrome:
                    init_script += "\n\n" + get_chrome_emulation_bundle()

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
