import asyncio
import os
import json
import uuid
import time
from src.fingerprint_engine.api.fingerprint_service import fingerprint_service
from src.camo.security.fingerprint_validator import fingerprint_validator
from src.runtime_spoofer.core.runtime_injector import runtime_injector

def generate_mock_profile():
    prof_id = str(uuid.uuid4())
    fp = fingerprint_service.create_fingerprint(prof_id, "windows")
    return prof_id, fp

async def run_integrity_test():
    print("--- CAMO System Integrity Test ---")
    start = time.perf_counter()

    prof_id, fp = generate_mock_profile()
    val = fingerprint_validator.validate(fp)
    if val["status"] != "valid":
        print("FAIL: Fingerprint validation failed", val)
        return

    print("PASS: Fingerprint Generation & Validation")

    # Try bundling scripts
    from src.screen_spoofer.core.screen_injector import screen_injector
    script = screen_injector.get_injection_script()
    if "spoofedOuterWidth" not in script:
        print("FAIL: JS Script bundling failed")
        return

    print("PASS: Runtime Module Bundling")

    end = time.perf_counter()
    print(f"Total logic integrity test duration: {(end - start)*1000:.2f}ms")

if __name__ == "__main__":
    asyncio.run(run_integrity_test())
