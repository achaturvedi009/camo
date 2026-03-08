def generate_permission_rules(fingerprint: dict) -> dict:
    """
    Maps fingerprint parameters to realistic permission states.
    For instance, macOS might handle certain permissions differently than Windows.
    """
    os_type = fingerprint.get("platform", "").lower()

    # Default stealth rules
    rules = {
        "notifications": "default",
        "geolocation": "prompt",
        "camera": "prompt",
        "microphone": "prompt",
        "clipboard-read": "prompt",
        "clipboard-write": "granted",
        "midi": "prompt",
        "background-sync": "granted",
        "accelerometer": "granted",
        "gyroscope": "granted",
        "magnetometer": "granted",
        "payment-handler": "granted",
        "persistent-storage": "prompt"
    }

    # Example of varying based on fingerprint
    if "mac" in os_type:
        rules["payment-handler"] = "prompt" # Apple Pay environments

    return rules
