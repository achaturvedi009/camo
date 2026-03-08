from typing import Optional
from src.fingerprint_engine.core.seed_engine import SeedEngine
from src.fingerprint_engine.core.dataset_loader import DatasetManager
from src.fingerprint_engine.network.ip_geolocation import get_location_for_ip
from src.fingerprint_engine.generators.canvas_generator import generate_canvas
from src.fingerprint_engine.generators.webgl_generator import generate_webgl
from src.fingerprint_engine.generators.audio_generator import generate_audio
from src.fingerprint_engine.tls.tls_fingerprint import generate_tls_fingerprint
from src.fingerprint_engine.models.fingerprint_model import FingerprintModel

class FingerprintBuilder:
    def __init__(self, profile_id: str, os_type: str, ip_address: Optional[str] = None):
        self.engine = SeedEngine(profile_id)
        self.profile_id = profile_id
        self.os_type = os_type.lower()
        self.ip_address = ip_address

    def build(self) -> dict:
        # Layer 1: Network & Timezone
        if self.ip_address:
            geo_data = get_location_for_ip(self.ip_address)
            country = geo_data.get("country", "US")
            timezone = geo_data.get("timezone", self.engine.pick(DatasetManager.get_timezones().get("US", ["America/New_York"])))
        else:
            all_tzs = []
            for tzs in DatasetManager.get_timezones().values():
                all_tzs.extend(tzs)
            timezone = self.engine.pick(all_tzs)
            country = "Unknown"

        locale = "en-US"

        network = {
            "public_ip": self.ip_address,
            "country": country,
            "region": None,
            "city": None,
            "asn": None,
            "isp": None,
            "timezone": timezone,
            "locale": locale,
            "webrtc_protection": "proxy",
            "dns_leak_protection": True,
            "proxy_verification": True
        }

        # Layer 4: Hardware Base
        cpus = DatasetManager.get_cpus()
        rams = DatasetManager.get_rams()
        screens = DatasetManager.get_screens()

        all_gpus = DatasetManager.get_gpus()
        valid_gpus = [g for g in all_gpus if self.os_type in g.get("os", [])]
        if not valid_gpus: valid_gpus = all_gpus

        gpu = self.engine.pick(valid_gpus, offset=10)
        cpu = self.engine.pick(cpus, offset=11)
        ram = self.engine.pick(rams, offset=12)
        screen = self.engine.pick(screens, offset=13)

        # Layer 2 & 3: User Agent, Navigator, Headers
        uas = DatasetManager.get_user_agents()
        valid_uas = [ua for ua in uas if self.os_type == ua.get("os", "")]
        if not valid_uas: valid_uas = uas
        ua_obj = self.engine.pick(valid_uas, offset=14)
        ua_str = ua_obj["ua"]

        if self.os_type == "windows":
            platform = "Win32"
            touch_support = False
        elif self.os_type == "mac":
            platform = "MacIntel"
            touch_support = False
        elif self.os_type == "linux":
            platform = "Linux x86_64"
            touch_support = False
        else:
            platform = "Linux armv8l"
            touch_support = True

        languages = self.engine.pick(DatasetManager.get_languages(), offset=15)

        navigator = {
            "userAgent": ua_str,
            "platform": platform,
            "languages": languages,
            "hardwareConcurrency": cpu,
            "deviceMemory": ram,
            "maxTouchPoints": 5 if touch_support else 0,
            "vendor": "Google Inc." if "Chrome" in ua_str else "",
            "productSub": "20030107" if "Firefox" not in ua_str else "20100101",
            "webdriver": False,
            "plugins": [{"name": "Chrome PDF Plugin", "filename": "internal-pdf-viewer"}],
            "mimeTypes": [{"type": "application/pdf", "suffixes": "pdf"}]
        }

        headers = {
            "user_agent": ua_str,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept_language": f"{languages[0]},{languages[1]};q=0.9" if len(languages) > 1 else languages[0],
            "accept_encoding": "gzip, deflate, br",
            "connection": "keep-alive",
            "upgrade_insecure_requests": "1",
            "sec_ch_ua": '"Not/A)Brand";v="99", "Google Chrome";v="123", "Chromium";v="123"',
            "sec_ch_ua_mobile": "?1" if touch_support else "?0",
            "sec_ch_ua_platform": f'"{platform}"',
            "sec_fetch_site": "none",
            "sec_fetch_mode": "navigate",
            "sec_fetch_dest": "document"
        }

        hardware = {
            "cpu_cores": cpu,
            "ram": ram,
            "gpu_vendor": gpu["vendor"],
            "gpu_renderer": gpu["renderer"],
            "devicePixelRatio": screen["pixelRatio"],
            "touch_support": touch_support,
            "screen_resolution": f"{screen['width']}x{screen['height']}",
            "color_depth": screen["colorDepth"]
        }

        # Layer 5: Rendering
        webgl_prof = self.engine.pick(DatasetManager.get_webgl_profiles(), offset=16)

        webgl_hash = generate_webgl(self.engine, gpu)
        webgl_model = {
            "vendor": gpu["vendor"],
            "renderer": gpu["renderer"],
            "shader_precision": webgl_prof["shader_precision"],
            "supported_extensions": webgl_prof["extensions"],
            "max_texture_size": webgl_prof["max_texture_size"],
            "anisotropic_filtering": True
        }

        rendering = {
            "canvas_hash": generate_canvas(self.engine),
            "webgl": webgl_model,
            "audio_hash": generate_audio(self.engine)
        }

        # Layer 6: Environment
        fonts = DatasetManager.get_fonts(self.os_type)
        environment = {
            "timezone": timezone,
            "locale": languages[0],
            "languages": languages,
            "fonts": fonts,
            "media_codecs": ["video/mp4", "audio/mp3", "video/webm"],
            "color_depth": screen["colorDepth"]
        }

        # Layer 7: Behavioral
        behavioral = {
            "mouse_movement_curves": "human_standard",
            "scroll_acceleration": self.engine.random_float(0.8, 1.2, offset=17),
            "typing_delay_mean": self.engine.random_int(80, 150, offset=18),
            "click_interval_mean": self.engine.random_int(100, 250, offset=19)
        }

        # Layer 8: TLS
        tls = generate_tls_fingerprint(self.engine, ua_obj["browser"])

        fp_dict = {
            "profile_id": self.profile_id,
            "network": network,
            "headers": headers,
            "navigator": navigator,
            "hardware": hardware,
            "rendering": rendering,
            "environment": environment,
            "behavioral": behavioral,
            "tls": tls
        }

        # Validates model serialization
        return FingerprintModel(**fp_dict).model_dump()
