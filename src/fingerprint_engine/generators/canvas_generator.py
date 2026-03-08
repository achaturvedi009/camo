from src.fingerprint_engine.core.seed_engine import SeedEngine

def generate_canvas(seed_engine: SeedEngine) -> str:
    """Simulates realistic deterministic canvas noise injection using SHA-256."""
    return seed_engine.deterministic_hash("canvas_render", offset=7)
