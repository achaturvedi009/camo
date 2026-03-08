class ProxyIpManager:
    @staticmethod
    def get_proxy_ip(fingerprint: dict) -> str:
        """
        Extracts the proxy IP from the fingerprint mapping or falls back safely.
        """
        if "network" in fingerprint:
            return fingerprint["network"].get("public_ip", "0.0.0.0")
        return "0.0.0.0"

    @staticmethod
    def get_webrtc_mode(fingerprint: dict) -> str:
        """
        Extracts the webrtc protection mode: disabled, proxy-only, strict-mask
        """
        if "network" in fingerprint:
            return fingerprint["network"].get("webrtc_protection", "proxy-only")
        return "proxy-only"
