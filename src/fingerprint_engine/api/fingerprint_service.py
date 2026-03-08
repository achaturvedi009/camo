from typing import Optional
from src.fingerprint_engine.core.fingerprint_builder import FingerprintBuilder
from src.fingerprint_engine.validators.consistency_validator import validate

class FingerprintService:
    @staticmethod
    def create_fingerprint(profile_id: str, os_type: str = "windows", ip_address: Optional[str] = None) -> dict:
        builder = FingerprintBuilder(profile_id, os_type, ip_address)
        fp = builder.build()

        # Backward compatibility with older components (Runtime Injector)
        # We merge old flat structure into the root so old JS scripts still work,
        # while the new backend has the deeply nested dictionary.

        flat_fp = {
            "userAgent": fp["navigator"]["userAgent"],
            "platform": fp["navigator"]["platform"],
            "cpu": fp["hardware"]["cpu_cores"],
            "ram": fp["hardware"]["ram"],
            "gpuVendor": fp["hardware"]["gpu_vendor"],
            "gpuRenderer": fp["hardware"]["gpu_renderer"],
            "screen": fp["hardware"]["screen_resolution"],
            "devicePixelRatio": fp["hardware"]["devicePixelRatio"],
            "timezone": fp["environment"]["timezone"],
            "languages": fp["environment"]["languages"],
            "webglHash": fp["rendering"]["webgl"]["renderer"], # mapped to renderer to satisfy webgl_spoofer.js
            "canvasHash": fp["rendering"]["canvas_hash"],
            "audioHash": fp["rendering"]["audio_hash"],
            "fonts": fp["environment"]["fonts"],
            "touchSupport": fp["hardware"]["touch_support"],
            "tls": fp["tls"]
        }

        # Add the nested structure under a key if needed, or just return flat for now since
        # the prompt asks to return the specific output format.
        return flat_fp

    @staticmethod
    def load_fingerprint(profile_id: str):
        pass

    @staticmethod
    def validate_fingerprint(fingerprint: dict) -> bool:
        return validate(fingerprint)

fingerprint_service = FingerprintService()
