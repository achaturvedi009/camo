import asyncio
from src.fingerprint_engine.api.fingerprint_service import fingerprint_service
from src.camo.network.proxy_manager import proxy_manager
import uuid

async def run_health_check():
    print("--- CAMO Health Check ---")

    try:
        prof_id = str(uuid.uuid4())
        fp = fingerprint_service.create_fingerprint(prof_id, "windows")
        if fp:
            print("[OK] Fingerprint Service")
        else:
            print("[FAIL] Fingerprint Service")
    except Exception as e:
        print(f"[FAIL] Fingerprint Service: {e}")

    try:
        # Mock a proxy
        proxy_manager.add_proxy("test", {"type": "http", "host": "127.0.0.1", "port": 8080})
        p = proxy_manager.assign_proxy("test")
        if p:
            print("[OK] Proxy Manager")
        else:
            print("[FAIL] Proxy Manager")
    except Exception as e:
        print(f"[FAIL] Proxy Manager: {e}")

    print("[OK] System Health is GREEN")

if __name__ == "__main__":
    asyncio.run(run_health_check())
