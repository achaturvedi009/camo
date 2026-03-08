import random
from typing import Dict, Any

class FingerprintGenerator:
    def __init__(self):
        self.presets = {
            "windows": {
                "userAgents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                ],
                "platform": "Win32",
                "screens": [{"width": 1920, "height": 1080}, {"width": 1366, "height": 768}, {"width": 2560, "height": 1440}],
                "webgl": [
                    {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
                    {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)"}
                ],
                "touchSupport": False,
                "deviceMemory": [8, 16, 32],
                "hardwareConcurrency": [4, 8, 12, 16]
            },
            "linux": {
                "userAgents": [
                    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                ],
                "platform": "Linux x86_64",
                "screens": [{"width": 1920, "height": 1080}, {"width": 1280, "height": 800}],
                "webgl": [
                    {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Mesa Intel(R) UHD Graphics 620 (KBL GT2), OpenGL 4.6)"},
                    {"vendor": "NVIDIA Corporation", "renderer": "NVIDIA GeForce RTX 3060/PCIe/SSE2"}
                ],
                "touchSupport": False,
                "deviceMemory": [4, 8, 16],
                "hardwareConcurrency": [4, 8, 12]
            },
            "android": {
                "userAgents": [
                    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
                    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"
                ],
                "platform": "Android",
                "screens": [{"width": 360, "height": 800}, {"width": 412, "height": 915}],
                "webgl": [
                    {"vendor": "Qualcomm", "renderer": "Adreno (TM) 740"},
                    {"vendor": "ARM", "renderer": "Mali-G710"}
                ],
                "touchSupport": True,
                "deviceMemory": [4, 6, 8],
                "hardwareConcurrency": [8]
            }
        }
        self.timezones = ["America/New_York", "Europe/London", "Asia/Kolkata", "America/Los_Angeles", "Europe/Berlin", "Asia/Tokyo"]
        self.languages = [["en-US", "en"], ["en-GB", "en"], ["de-DE", "de", "en-US", "en"], ["hi-IN", "hi", "en-US", "en"]]

    def generate(self, os_type: str = "windows") -> Dict[str, Any]:
        preset = self.presets.get(os_type.lower(), self.presets["windows"])

        # Apply standard randomness within realistic ranges
        return {
            "userAgent": random.choice(preset["userAgents"]),
            "platform": preset["platform"],
            "screen": random.choice(preset["screens"]),
            "timezone": random.choice(self.timezones),
            "webgl": random.choice(preset["webgl"]),
            "languages": random.choice(self.languages),
            "deviceMemory": random.choice(preset["deviceMemory"]),
            "hardwareConcurrency": random.choice(preset["hardwareConcurrency"]),
            "touchSupport": preset["touchSupport"],
            "canvasNoise": round(random.uniform(0.000001, 0.00005), 8),
            "audioNoise": round(random.uniform(0.000001, 0.00005), 8)
        }

fingerprint_generator = FingerprintGenerator()
