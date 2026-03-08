import os
import json
import uuid
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from src.core.db import SessionLocal, ProfileModel
import datetime
import shutil

PROFILES_DIR = "data/profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)

class ProxyConfig(BaseModel):
    type: str = "http"
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    icon: str = "🦊"
    tags: List[str] = []
    proxy: Optional[ProxyConfig] = None
    os: str = "windows"
    camoufox_version: Optional[str] = None
    fingerprint: Optional[Dict] = None
    created_at: float = 0.0

class ProfileManager:
    def __init__(self, data_dir: str = "data"):
        self.profiles_dir = os.path.join(data_dir, "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)

    def _db_to_pydantic(self, db_prof: ProfileModel) -> Profile:
        proxy = None
        if db_prof.proxy_enabled:
            proxy = ProxyConfig(
                type=db_prof.proxy_type,
                host=db_prof.proxy_host,
                port=db_prof.proxy_port,
                username=db_prof.proxy_username,
                password=db_prof.proxy_password
            )

        tags = [t.strip() for t in db_prof.tags.split(',')] if db_prof.tags else []
        return Profile(
            id=db_prof.id,
            name=db_prof.name,
            icon=db_prof.icon,
            tags=tags,
            os=db_prof.os_type,
            camoufox_version=db_prof.camoufox_version,
            fingerprint=db_prof.fingerprint,
            proxy=proxy,
            created_at=db_prof.created_at.timestamp() if db_prof.created_at else 0.0
        )

    def _pydantic_to_db(self, prof: Profile, db_prof: ProfileModel):
        db_prof.id = prof.id
        db_prof.name = prof.name
        db_prof.icon = prof.icon
        db_prof.tags = ",".join(prof.tags) if prof.tags else ""
        db_prof.os_type = prof.os
        db_prof.camoufox_version = prof.camoufox_version
        db_prof.fingerprint = prof.fingerprint

        if prof.proxy:
            db_prof.proxy_enabled = True
            db_prof.proxy_type = prof.proxy.type
            db_prof.proxy_host = prof.proxy.host
            db_prof.proxy_port = prof.proxy.port
            db_prof.proxy_username = prof.proxy.username
            db_prof.proxy_password = prof.proxy.password
        else:
            db_prof.proxy_enabled = False
            db_prof.proxy_type = None
            db_prof.proxy_host = None
            db_prof.proxy_port = None
            db_prof.proxy_username = None
            db_prof.proxy_password = None

    def create_profile(self, name: str, tags: List[str] = None, proxy: Optional[ProxyConfig] = None, os_type: str = "windows", camoufox_version: str = None, fingerprint: dict = None) -> Profile:
        prof_id = str(uuid.uuid4())
        prof = Profile(
            id=prof_id,
            name=name,
            tags=tags or [],
            proxy=proxy,
            os=os_type,
            camoufox_version=camoufox_version,
            fingerprint=fingerprint,
            created_at=datetime.datetime.utcnow().timestamp()
        )

        db = SessionLocal()
        db_prof = ProfileModel()
        self._pydantic_to_db(prof, db_prof)
        db.add(db_prof)
        db.commit()
        db.close()
        return prof

    def update_profile(self, profile_id: str, updates: Dict) -> Optional[Profile]:
        db = SessionLocal()
        db_prof = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not db_prof:
            db.close()
            return None

        prof = self._db_to_pydantic(db_prof)

        if "name" in updates: prof.name = updates["name"]
        if "icon" in updates: prof.icon = updates["icon"]
        if "tags" in updates: prof.tags = updates["tags"]
        if "os" in updates: prof.os = updates["os"]
        if "camoufox_version" in updates: prof.camoufox_version = updates["camoufox_version"]
        if "fingerprint" in updates: prof.fingerprint = updates["fingerprint"]

        if "proxy" in updates:
            if updates["proxy"] is None:
                prof.proxy = None
            elif isinstance(updates["proxy"], dict):
                prof.proxy = ProxyConfig(**updates["proxy"])
            elif isinstance(updates["proxy"], ProxyConfig):
                prof.proxy = updates["proxy"]

        self._pydantic_to_db(prof, db_prof)
        db.commit()
        db.close()
        return prof

    def delete_profile(self, profile_id: str) -> bool:
        db = SessionLocal()
        db_prof = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if db_prof:
            db.delete(db_prof)
            db.commit()
            db.close()
            profile_dir = self.get_profile_dir(profile_id)
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
            return True
        db.close()
        return False

    def get_profile(self, profile_id: str) -> Optional[Profile]:
        db = SessionLocal()
        db_prof = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if db_prof:
            prof = self._db_to_pydantic(db_prof)
            db.close()
            return prof
        db.close()
        return None

    def list_profiles(self) -> List[Profile]:
        db = SessionLocal()
        db_profs = db.query(ProfileModel).all()
        profs = [self._db_to_pydantic(p) for p in db_profs]
        db.close()
        return profs

    def get_profile_dir(self, profile_id: str) -> str:
        return os.path.join(self.profiles_dir, profile_id)

profile_manager = ProfileManager()
