import os
import json
import uuid
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

PROFILES_DIR = "data/profiles"

class ProxyConfig(BaseModel):
    type: str = "http" # http, https, socks4, socks5
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

class FingerprintConfig(BaseModel):
    os: str = "windows" # windows, linux, android
    screen_width: int = 1920
    screen_height: int = 1080

class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    icon: str = "🦊"
    tags: List[str] = []
    proxy: Optional[ProxyConfig] = None
    os: str = "windows"
    created_at: float = 0.0

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.profiles_file = os.path.join(data_dir, "profiles.json")
        self.profiles_dir = os.path.join(data_dir, "profiles")
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.profiles_dir, exist_ok=True)
        self.profiles: Dict[str, Profile] = {}
        self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, "r") as f:
                data = json.load(f)
                for item in data:
                    profile = Profile(**item)
                    self.profiles[profile.id] = profile

    def _save_profiles(self):
        data = [p.model_dump() for p in self.profiles.values()]
        with open(self.profiles_file, "w") as f:
            json.dump(data, f, indent=2)

    def create_profile(self, name: str, tags: List[str] = None, proxy: Optional[ProxyConfig] = None, os_type: str = "windows") -> Profile:
        import time
        profile = Profile(
            name=name,
            tags=tags or [],
            proxy=proxy,
            os=os_type,
            created_at=time.time()
        )
        self.profiles[profile.id] = profile
        self._save_profiles()
        return profile

    def update_profile(self, profile_id: str, updates: Dict) -> Optional[Profile]:
        if profile_id not in self.profiles:
            return None
        profile = self.profiles[profile_id]

        # Apply updates
        if "name" in updates:
            profile.name = updates["name"]
        if "icon" in updates:
            profile.icon = updates["icon"]
        if "tags" in updates:
            profile.tags = updates["tags"]
        if "proxy" in updates:
            if updates["proxy"] is None:
                profile.proxy = None
            else:
                profile.proxy = ProxyConfig(**updates["proxy"])
        if "os" in updates:
            profile.os = updates["os"]

        self.profiles[profile_id] = profile
        self._save_profiles()
        return profile

    def delete_profile(self, profile_id: str) -> bool:
        if profile_id in self.profiles:
            del self.profiles[profile_id]
            self._save_profiles()
            import shutil
            profile_dir = self.get_profile_dir(profile_id)
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
            return True
        return False

    def get_profile(self, profile_id: str) -> Optional[Profile]:
        return self.profiles.get(profile_id)

    def list_profiles(self) -> List[Profile]:
        return list(self.profiles.values())

    def get_profile_dir(self, profile_id: str) -> str:
        return os.path.join(self.profiles_dir, profile_id)

profile_manager = ProfileManager()
