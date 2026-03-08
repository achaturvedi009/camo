from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class NetworkModel(BaseModel):
    public_ip: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    asn: Optional[str] = None
    isp: Optional[str] = None
    timezone: str
    locale: str
    webrtc_protection: str = "proxy" # disable, proxy, mask
    dns_leak_protection: bool = True
    proxy_verification: bool = True

class HttpHeadersModel(BaseModel):
    user_agent: str
    accept: str
    accept_language: str
    accept_encoding: str
    connection: str
    upgrade_insecure_requests: str
    sec_ch_ua: str
    sec_ch_ua_mobile: str
    sec_ch_ua_platform: str
    sec_fetch_site: str
    sec_fetch_mode: str
    sec_fetch_dest: str

class NavigatorModel(BaseModel):
    userAgent: str
    platform: str
    languages: List[str]
    hardwareConcurrency: int
    deviceMemory: int
    maxTouchPoints: int
    vendor: str
    productSub: str
    webdriver: bool = False
    plugins: List[Dict[str, str]]
    mimeTypes: List[Dict[str, str]]

class HardwareModel(BaseModel):
    cpu_cores: int
    ram: int
    gpu_vendor: str
    gpu_renderer: str
    devicePixelRatio: float
    touch_support: bool
    screen_resolution: str
    color_depth: int

class WebGLModel(BaseModel):
    vendor: str
    renderer: str
    shader_precision: str
    supported_extensions: List[str]
    max_texture_size: int
    anisotropic_filtering: bool

class RenderingModel(BaseModel):
    canvas_hash: str
    webgl: WebGLModel
    audio_hash: str

class EnvironmentModel(BaseModel):
    timezone: str
    locale: str
    languages: List[str]
    fonts: List[str]
    media_codecs: List[str]
    color_depth: int

class BehavioralModel(BaseModel):
    mouse_movement_curves: str = "human_standard"
    scroll_acceleration: float
    typing_delay_mean: int
    click_interval_mean: int

class TlsModel(BaseModel):
    ja3: str
    cipher_suites: List[str]
    extensions: List[str]
    alpn: List[str]

class FingerprintModel(BaseModel):
    profile_id: str
    network: NetworkModel
    headers: HttpHeadersModel
    navigator: NavigatorModel
    hardware: HardwareModel
    rendering: RenderingModel
    environment: EnvironmentModel
    behavioral: BehavioralModel
    tls: TlsModel
