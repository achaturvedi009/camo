from src.fingerprint_engine.core.seed_engine import SeedEngine

def generate_tls_fingerprint(seed_engine: SeedEngine, browser: str) -> dict:
    """Simulates TLS signatures like JA3."""
    ja3 = seed_engine.deterministic_hash(f"ja3_{browser}", offset=42)
    return {
        "ja3": ja3,
        "cipher_suites": ["TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"],
        "extensions": ["server_name", "supported_groups", "ec_point_formats", "signature_algorithms", "alpn"],
        "alpn": ["h2", "http/1.1"]
    }
