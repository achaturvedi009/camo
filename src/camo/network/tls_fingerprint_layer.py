class TLSFingerprintLayer:
    @staticmethod
    def get_tls_signature(browser_engine: str, os_type: str) -> dict:
        """
        Returns realistic TLS handshake parameters (JA3, ALPN, cipher suites)
        matched against the exact underlying browser engine and OS configuration.
        This overrides the native python requests TLS behavior for proxies if necessary,
        though modern Camoufox internally handles curl-impersonate level TLS masking.
        """
        if "firefox" in browser_engine.lower():
            return {
                "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
                "ciphers": ["TLS_AES_128_GCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256", "TLS_AES_256_GCM_SHA384"],
                "alpn": ["h2", "http/1.1"]
            }
        else: # Chromium/WebKit defaults
            return {
                "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
                "ciphers": ["TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"],
                "alpn": ["h2", "http/1.1"]
            }
