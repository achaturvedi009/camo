from src.canvas_spoofer.core.seed_manager import get_canvas_seed

def integrate_canvas_seed(fingerprint: dict, profile_id: str) -> dict:
    """
    Ensures the canvasHash is properly synced with the isolated Canvas Spoofer subsystem.
    """
    fingerprint["canvasHash"] = get_canvas_seed(profile_id)
    return fingerprint
