from src.webrtc_protector.core.proxy_ip_manager import ProxyIpManager

def integrate_webrtc_config(fingerprint: dict, active_proxy_host: str = None) -> dict:
    """
    Ensures network structures correctly map into the JSON injected globally on window object context.
    """
    if "network" not in fingerprint:
        fingerprint["network"] = {}

    fingerprint["network"]["webrtc_protection"] = "proxy-only"

    if active_proxy_host:
        fingerprint["network"]["public_ip"] = active_proxy_host
    elif "public_ip" not in fingerprint["network"]:
        fingerprint["network"]["public_ip"] = "0.0.0.0"

    return fingerprint
