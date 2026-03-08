from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from src.core.profile_manager import profile_manager, Profile, ProxyConfig
from src.core.browser import browser_manager
from src.core.proxy_tester import test_proxy

app = FastAPI(title="Antidetect Browser API")

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

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    tags: Optional[List[str]] = None
    proxy: Optional[ProxyConfig] = None
    os: Optional[str] = None

class ProxyTestRequest(BaseModel):
    type: str = "http"
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

@app.get("/profiles", response_model=List[Profile])
def list_profiles():
    return profile_manager.list_profiles()

@app.post("/profiles", response_model=Profile)
def create_profile(profile_in: ProfileCreate):
    return profile_manager.create_profile(
        name=profile_in.name,
        tags=profile_in.tags,
        proxy=profile_in.proxy,
        os_type=profile_in.os
    )

@app.put("/profiles/{profile_id}", response_model=Profile)
def update_profile(profile_id: str, updates: ProfileUpdate):
    update_dict = {k: v for k, v in updates.model_dump().items() if v is not None}
    profile = profile_manager.update_profile(profile_id, update_dict)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: str):
    success = profile_manager.delete_profile(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"status": "success"}

@app.post("/profiles/{profile_id}/start")
def start_profile(profile_id: str):
    try:
        browser_manager.start_profile(profile_id)
        return {"status": "started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/profiles/{profile_id}/stop")
def stop_profile(profile_id: str):
    success = browser_manager.stop_profile(profile_id)
    if not success:
        return {"status": "not_running"}
    return {"status": "stopped"}

@app.get("/profiles/{profile_id}/status")
def get_profile_status(profile_id: str):
    running = browser_manager.is_running(profile_id)
    return {"running": running}

@app.post("/proxy/test")
def test_proxy_route(req: ProxyTestRequest):
    success = test_proxy(
        proxy_type=req.type,
        host=req.host,
        port=req.port,
        username=req.username,
        password=req.password
    )
    return {"success": success}
