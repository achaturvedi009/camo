from src.fingerprint_engine.api.fingerprint_service import fingerprint_service
import json
import time

print("Generating 10 unique fingerprints deterministically...")
start = time.perf_counter()

for i in range(10):
    profile_id = f"camo_user_{i}"
    # We can pass random IPs to test geo-loc or None
    fp = fingerprint_service.create_fingerprint(profile_id, os_type="mac")
    print(f"\n--- Profile {i} ---")
    print(f"UA: {fp['userAgent']}")
    print(f"Hardware: {fp['cpu']} Cores, {fp['ram']}GB RAM")
    print(f"GPU: {fp['gpuVendor']} - {fp['gpuRenderer']}")
    print(f"Webgl Hash: {fp['webglHash']}")
    print(f"Screen: {fp['screen']}")

end = time.perf_counter()
print(f"\nTotal generation time: {(end - start) * 1000:.2f}ms")
