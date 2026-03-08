# CAMO Fingerprint Engine Integration Guide

The next-generation enterprise-grade fingerprint engine is designed to seamlessly integrate into the CAMO browser orchestration system. It achieves perfect determinism via `profile_id` seeding and realistic evasion of advanced detectors.

## Using the Engine

```python
from src.fingerprint_engine.api.fingerprint_service import fingerprint_service
import json

profile_id = "test-profile-123"
proxy_ip = "104.16.123.45" # Example Cloudflare IP
os_spoof = "windows"

# Generate a fingerprint matching the IP's Timezone and OS preference
fingerprint = fingerprint_service.create_fingerprint(
    profile_id=profile_id,
    os_type=os_spoof,
    ip_address=proxy_ip
)

print(json.dumps(fingerprint, indent=2))
```

## Runtime Injection
To use the fingerprint output in a Playwright session with CAMO's `RuntimeInjector`:

```python
from src.runtime_spoofer.core.runtime_injector import runtime_injector

# Construct JS bundle with properties matching the exact fingerprint
js_bundle = runtime_injector.build_init_script(fingerprint)

# Pass it to your Playwright Context
await browser_context.add_init_script(js_bundle)
```

## Available Datasets
The datasets (`src/fingerprint_engine/datasets/`) include:
- CPUs & RAMs
- Fonts (Mac, Linux, Windows)
- Real GPU Renderers
- User Agents & Languages
- Timezones linked to Country codes
- Audio and WebGL Profiles
