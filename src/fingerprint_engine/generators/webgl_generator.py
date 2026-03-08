from src.fingerprint_engine.core.seed_engine import SeedEngine
from typing import Dict

def generate_webgl(seed_engine: SeedEngine, gpu_info: Dict) -> str:
    """Simulates realistic WebGL extension strings and properties hashed."""
    vendor = gpu_info["vendor"]
    renderer = gpu_info["renderer"]
    base_str = f"webgl_{vendor}_{renderer}"
    return seed_engine.deterministic_hash(base_str, offset=13)
