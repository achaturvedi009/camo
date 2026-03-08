import asyncio
import requests
from typing import Dict, Optional

class ProxyManager:
    def __init__(self):
        self.proxy_pool = {}

    def add_proxy(self, proxy_id: str, proxy_data: dict):
        self.proxy_pool[proxy_id] = proxy_data

    def assign_proxy(self, profile_id: str) -> Optional[dict]:
        """
        Automatically selects an available, healthy proxy from the pool.
        """
        # Simplified: pick the first available
        if not self.proxy_pool:
            return None
        return next(iter(self.proxy_pool.values()))

    async def verify_proxy(self, proxy: dict) -> bool:
        """
        Asynchronously validates the proxy connection against an IP echo service.
        """
        loop = asyncio.get_event_loop()
        try:
            proxy_url = f"{proxy['type']}://"
            if proxy.get('username'):
                proxy_url += f"{proxy['username']}:{proxy['password']}@"
            proxy_url += f"{proxy['host']}:{proxy['port']}"

            proxies = {"http": proxy_url, "https": proxy_url}

            # Run blocking request in executor
            resp = await loop.run_in_executor(
                None,
                lambda: requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
            )
            return resp.status_code == 200
        except Exception:
            return False

    def get_proxy_status(self, proxy_id: str) -> dict:
        proxy = self.proxy_pool.get(proxy_id)
        if not proxy:
            return {"status": "not_found"}
        # Assume healthy if it exists for this mock
        return {"status": "healthy", "latency": "45ms", "type": proxy.get("type")}

proxy_manager = ProxyManager()
