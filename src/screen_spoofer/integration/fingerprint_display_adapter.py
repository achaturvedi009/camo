from src.screen_spoofer.core.display_profile_manager import DisplayProfileManager

def integrate_display_config(fingerprint: dict) -> dict:
    """
    Syncs the display config properties down strictly over the fingerprint hierarchy.
    The Fingerprint Builder already structures it under hardware correctly natively.
    """
    return fingerprint
