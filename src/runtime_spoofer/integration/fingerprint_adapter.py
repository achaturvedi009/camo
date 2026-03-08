import json

def generate_injection_script(fingerprint_data: dict) -> str:
    """
    Takes a dict representing the fingerprint profile and wraps it inside
    a JavaScript snippet that exposes it to `window.__CAMO_FP__`.
    """
    safe_json = json.dumps(fingerprint_data)
    script = f"""
    Object.defineProperty(window, '__CAMO_FP__', {{
        value: {safe_json},
        writable: false,
        enumerable: false,
        configurable: false
    }});
    """
    return script
