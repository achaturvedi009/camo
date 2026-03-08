from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import os
import json

router = APIRouter()

# Need to map to existing profile DB, but for encapsulation we'll mock or load directly
from src.core.profile_manager import profile_manager

@router.get("/profile-info/{profile_id}")
def get_profile_diagnostic(profile_id: str):
    prof = profile_manager.get_profile(profile_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")

    fp = prof.fingerprint or {}
    hw = fp.get("hardware", {})
    net = fp.get("network", {})
    nav = fp.get("navigator", {})
    rend = fp.get("rendering", {})
    env = fp.get("environment", {})

    return {
        "ip": net.get("public_ip", "0.0.0.0"),
        "country": net.get("country", "Unknown"),
        "timezone": env.get("timezone", "UTC"),
        "browser": "Chromium 120 (Spoofed)",
        "userAgent": nav.get("userAgent", ""),
        "platform": nav.get("platform", ""),
        "cpu": hw.get("cpu_cores", 4),
        "ram": hw.get("ram", 8),
        "gpuVendor": hw.get("gpu_vendor", ""),
        "gpuRenderer": hw.get("gpu_renderer", ""),
        "screen": hw.get("screen_resolution", ""),
        "canvasHash": rend.get("canvas_hash", ""),
        "webglHash": rend.get("webgl", {}).get("renderer", ""),
        "audioHash": rend.get("audio_hash", ""),
        "webrtcIP": net.get("public_ip", "0.0.0.0")
    }

@router.get("/viewer", response_class=HTMLResponse)
def serve_dashboard_ui():
    base = os.path.dirname(__file__)
    html_path = os.path.join(base, "..", "frontend", "index.html")
    with open(html_path, 'r') as f:
        html = f.read()

    js_path = os.path.join(base, "..", "frontend", "dashboard.js")
    with open(js_path, 'r') as f:
        js = f.read()

    # Inject JS directly to avoid CORS/Static mapping during local runs simply
    html = html.replace('<script src="dashboard.js"></script>', f'<script>{js}</script>')
    return HTMLResponse(content=html, status_code=200)
