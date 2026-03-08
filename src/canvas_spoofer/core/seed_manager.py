import hashlib

def get_canvas_seed(profile_id: str) -> str:
    """
    Returns the SHA-256 seed specifically for the canvas generator subsystem.
    """
    return hashlib.sha256(f"canvas_override_{profile_id}".encode('utf-8')).hexdigest()
