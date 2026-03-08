from src.camo.profiles.profile_isolation import ProfileIsolationSystem
from src.camo.security.fingerprint_validator import fingerprint_validator
import asyncio

class BrowserController:
    """
    Enterprise facade orchestrating all CAMO subsystems before delegating to the low-level worker.
    """
    @staticmethod
    def launch(profile_id: str, fingerprint: dict, proxy: dict = None):
        validation = fingerprint_validator.validate(fingerprint)
        if validation["status"] == "invalid":
            raise ValueError(f"Fingerprint consistency check failed: {validation['reason']}")

        # Delegate down to existing browser manager
        from src.core.browser import browser_manager
        return browser_manager.start_profile(profile_id)

camo_browser_controller = BrowserController()
