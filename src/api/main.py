from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from src.core.profile_manager import profile_manager, Profile, ProxyConfig
from src.core.browser import browser_manager
from src.core.proxy_tester import test_proxy
from src.core.fingerprint import fingerprint_generator
from src.core.camoufox_version_manager import version_manager
import json

app = FastAPI(title="Antidetect Browser API")
from src.camo.dashboard.backend.dashboard_api import router as dashboard_router
app.include_router(dashboard_router, prefix="/dashboard-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileCreate(BaseModel):
    name: str
    tags: Optional[List[str]] = []
    proxy: Optional[ProxyConfig] = None
    os: Optional[str] = "windows"
    camoufox_version: Optional[str] = None
    fingerprint: Optional[Dict[str, Any]] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    tags: Optional[List[str]] = None
    proxy: Optional[ProxyConfig] = None
    os: Optional[str] = None
    camoufox_version: Optional[str] = None
    fingerprint: Optional[Dict[str, Any]] = None

class ProxyTestRequest(BaseModel):
    type: str = "http"
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

class GenerateFingerprintRequest(BaseModel):
    os: str = "windows"

class VersionInstallRequest(BaseModel):
    version: str

@app.get("/api/profiles", response_model=List[Profile])
def list_profiles():
    return profile_manager.list_profiles()

@app.post("/api/profiles", response_model=Profile)
def create_profile(profile_in: ProfileCreate):
    fp = profile_in.fingerprint
    if not fp:
        fp = fingerprint_generator.generate(profile_in.os)

    return profile_manager.create_profile(
        name=profile_in.name,
        tags=profile_in.tags,
        proxy=profile_in.proxy,
        os_type=profile_in.os,
        camoufox_version=profile_in.camoufox_version,
        fingerprint=fp
    )

@app.put("/api/profiles/{profile_id}", response_model=Profile)
def update_profile(profile_id: str, updates: ProfileUpdate):
    update_dict = {k: v for k, v in updates.model_dump().items() if v is not None}
    profile = profile_manager.update_profile(profile_id, update_dict)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.delete("/api/profiles/{profile_id}")
def delete_profile(profile_id: str):
    success = profile_manager.delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"status": "success"}

@app.post("/api/profiles/{profile_id}/launch")
def start_profile(profile_id: str):
    try:
        browser_manager.start_profile(profile_id)
        return {"status": "started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/profiles/{profile_id}/stop")
def stop_profile(profile_id: str):
    success = browser_manager.stop_profile(profile_id)
    if not success:
        return {"status": "not_running"}
    return {"status": "stopped"}

@app.post("/api/profiles/{profile_id}/clone", response_model=Profile)
def clone_profile(profile_id: str):
    prof = profile_manager.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")

    # New id and slight modifications
    fp = prof.fingerprint.copy() if prof.fingerprint else fingerprint_generator.generate(prof.os)
    fp["userAgent"] = fingerprint_generator.generate(prof.os)["userAgent"] # Give a new UA

    return profile_manager.create_profile(
        name=prof.name + " (Clone)",
        tags=prof.tags.copy(),
        proxy=prof.proxy,
        os_type=prof.os,
        camoufox_version=prof.camoufox_version,
        fingerprint=fp
    )

@app.get("/api/profiles/{profile_id}/export")
def export_profile(profile_id: str):
    prof = profile_manager.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")
    return prof.model_dump()

@app.post("/api/profiles/import")
def import_profile(profile_in: ProfileCreate):
    return create_profile(profile_in)

@app.get("/api/profiles/{profile_id}/status")
def get_profile_status(profile_id: str):
    running = browser_manager.is_running(profile_id)
    return {"running": running}

@app.post("/api/fingerprint/generate")
def generate_fingerprint_route(req: GenerateFingerprintRequest):
    return fingerprint_generator.generate(req.os)

@app.post("/api/fingerprint/regenerate/{profile_id}")
def regenerate_fingerprint(profile_id: str):
    prof = profile_manager.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")
    new_fp = fingerprint_generator.generate(prof.os)
    profile_manager.update_profile(profile_id, {"fingerprint": new_fp})
    return new_fp

@app.post("/api/proxy/test")
def test_proxy_route(req: ProxyTestRequest):
    success = test_proxy(
        proxy_type=req.type,
        host=req.host,
        port=req.port,
        username=req.username,
        password=req.password
    )
    return {"success": success}

# Camoufox Version APIs
@app.get("/api/camoufox/versions/available")
def get_available_versions():
    # Only return top 10 for speed
    v = version_manager.fetch_available_versions()
    return v[:10]

@app.get("/api/camoufox/versions/installed")
def get_installed_versions():
    return version_manager.get_installed_versions()

@app.post("/api/camoufox/versions/install")
def install_version(req: VersionInstallRequest):
    try:
        success = version_manager.install_version(req.version)
        return {"status": "success" if success else "failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/camoufox/versions/set-active")
def set_active_version(req: VersionInstallRequest):
    success = version_manager.set_active_version(req.version)
    return {"status": "success" if success else "failed"}

@app.delete("/api/camoufox/versions/{version}")
def uninstall_version(version: str):
    success = version_manager.uninstall_version(version)
    return {"status": "success" if success else "failed"}
