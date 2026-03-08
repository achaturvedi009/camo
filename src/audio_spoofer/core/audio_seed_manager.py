import hashlib

def get_audio_seed(profile_id: str) -> str:
    """
    Returns the SHA-256 seed specifically for the Audio context generator.
    """
    return hashlib.sha256(f"audio_context_override_{profile_id}".encode('utf-8')).hexdigest()
