from src.audio_spoofer.core.audio_seed_manager import get_audio_seed

def integrate_audio_seed(fingerprint: dict, profile_id: str) -> dict:
    """
    Syncs the underlying audio context hash parameters to the enterprise subsystem.
    """
    fingerprint["audioHash"] = get_audio_seed(profile_id)
    if "rendering" not in fingerprint:
        fingerprint["rendering"] = {}
    fingerprint["rendering"]["audio_hash"] = get_audio_seed(profile_id)
    return fingerprint
