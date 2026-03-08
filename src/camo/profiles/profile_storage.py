import os
import json
import time

class ProfileStorageSystem:
    def __init__(self, base_dir="data/camo_profiles"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def get_profile_path(self, profile_id: str) -> str:
        path = os.path.join(self.base_dir, profile_id)
        os.makedirs(path, exist_ok=True)
        return path

    def create_profile(self, profile_id: str, fingerprint: dict, proxy: dict = None) -> dict:
        path = self.get_profile_path(profile_id)

        meta = {
            "profile_id": profile_id,
            "creation_time": time.time(),
            "browser_engine": "chromium",
            "fingerprint_hash": fingerprint.get("canvasHash", "none")
        }

        self.update_profile(profile_id, "metadata.json", meta)
        self.update_profile(profile_id, "fingerprint.json", fingerprint)
        if proxy:
            self.update_profile(profile_id, "proxy.json", proxy)

        return meta

    def update_profile(self, profile_id: str, filename: str, data: dict):
        path = os.path.join(self.get_profile_path(profile_id), filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_profile(self, profile_id: str) -> dict:
        path = self.get_profile_path(profile_id)
        fp_path = os.path.join(path, "fingerprint.json")
        if not os.path.exists(fp_path):
            return None

        with open(fp_path, 'r') as f:
            fp = json.load(f)

        return {"id": profile_id, "fingerprint": fp}

profile_storage = ProfileStorageSystem()
