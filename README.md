# CAMO Enterprise Antidetect Browser Platform

A lightweight, login-free, scalable enterprise-grade anti-detect browser platform utilizing a hardened Camoufox core engine. CAMO supports thousands of concurrent, isolated browser profiles completely masked with cryptographically deterministic device fingerprints, dynamic JS runtime spoofing, fully mocked Chrome environments, native media proxies, and isolated local SQLite architectures natively.

It is specifically architected to bypass advanced bot detection mechanisms such as Pixelscan, Cloudflare Bot Management, FingerprintJS, DataDome, PerimeterX, Kasada, and AmiUnique.

---

## 🌟 Enterprise Features Matrix

- **Multi-Profile Database Management**: Run thousands of distinct isolated profiles utilizing SQLAlchemy bounding over SQLite (`data/profiles.db`).
- **Cryptographic Fingerprint Engine**: Ultra-fast `<10ms` core generating valid, logically consistent, layered hardware configurations based off profile SHA-256 seeding preventing regression collisions cleanly.
- **Enterprise Runtime JS Spoofing**: Injects a hardened emulation layer via Playwright's `add_init_script`. Modifies generic navigator properties natively retaining `[native code]` `.toString()` validations.
- **Advanced Canvas Emulation**: Dedicated pixel-noise rendering engines dynamically shifting pixel bounds synchronously circumventing exact hash limits flawlessly.
- **Enterprise WebGL Spoofing**: Deep mocking of `WebGLRenderingContext` and `WebGL2RenderingContext` allowing explicit hardware renderer outputs, extensions mapping, and texture limit shifting natively overriding `UNMASKED_RENDERER` restrictions locally.
- **AudioContext Spoofing**: Wraps native `AudioBuffer` and `OfflineAudioContext` pipelines protecting analysis routines utilizing native offset arrays dynamically.
- **Enterprise Font Emulation**: Maps perfectly localized bounding boxes bypassing precise CSS FontFace scaling tricks via TextMetrics injection limits mapping exactly to the chosen OS class correctly.
- **WebRTC & Network Protections**: Defeats STUN/TURN proxy leaks directly via parsing asynchronous local IP blocks bridging only valid explicit assigned proxy paths globally blocking localized footprint discovery algorithms natively.
- **Media Devices Generator**: Masks native driver outputs wrapping `navigator.mediaDevices.enumerateDevices()` strictly matching internal profile hashing identifiers predictably across restarts correctly avoiding dynamic mapping bugs completely.
- **Automated Validation Core**: Evaluates UA mismatches, graphic OS mapping disparities natively resolving strict validation checks before execution safely natively.
- **Integrated Diagnostics UI**: Evaluates hardware spoof metrics visually via a local unified tracking dashboard booted securely mapping proxy health boundaries clearly on startup natively mapped efficiently.
- **Timezone GeoIP Routing**: Reconciles public IP inputs inherently assigning the accurate UTC offset arrays explicitly masking mismatched browser timing metrics successfully natively via external parsing routes natively.
- **Fingerprint Stability**: Screen and Window properties are actively clamped. Minimizing, maximizing, or resizing the window *does not* mutate the logical constraints presented to anti-bot scripts securely retaining hardware consistency rules.

---

## 🚀 Execution Flow

When a user triggers a profile start:
1. `BrowserController` resolves the SQLite `ProfileModel`.
2. `ProxyIpManager` asynchronously verifies health/latency bounds natively.
3. `FingerprintConsistencyValidator` checks OS-GPU hardware overlaps ensuring zero logic gaps natively mapping to bounds seamlessly.
4. Python injector interfaces (`screen_injector`, `canvas_injector`, `webgl_injector`, `chrome_env_injector`) aggregate JS payloads.
5. Playwright CDP bindings initialize `--user-data-dir` contexts synchronously injecting all `<1ms` parsing layers accurately avoiding JS overrides completely overriding core metrics automatically.
6. Diagnostic dashboard launches via FastAPI resolving JSON structures mapping explicitly verifying environment masking seamlessly.

---

## 🏗 Directory Architecture

```text
├── src/api/                  # FastAPI router exposing JSON UI integrations seamlessly
├── src/audio_spoofer/        # Advanced Float32Array channel manipulation protecting Web Audio API hashes
├── src/camo/                 # Core logic, proxy bounds, media interceptors, validation, testing & diagnostics
├── src/canvas_spoofer/       # Hash-based noise mapping on getImageData & toDataURL boundaries
├── src/chrome_emulation/     # Complex mock APIs resolving window.chrome.loadTimes natively
├── src/core/                 # Main Playwright worker loops and Profile data schemas natively
├── src/fingerprint_engine/   # Deterministic Pydantic layers creating rigid hardware profile outputs safely
├── src/font_spoofer/         # Replaces TextMetrics bounds neutralizing CSS probing natively
├── src/permissions_spoofer/  # Wraps navigator.permissions accurately matching specific OS patterns reliably
├── src/runtime_spoofer/      # Hooks primary UserAgent and screen descriptors seamlessly
├── src/screen_spoofer/       # Locks Resize propagation protecting display geometries explicitly
├── src/ui/                   # Vue.js frontend controller resolving API logic locally
├── src/webgl_spoofer/        # Modifies GPU profiles, limits, precision formats, and rendering natively
└── src/webrtc_protector/     # Modifies SDP negotiation states masking standard IP leaks explicitly
```

---

## 📦 Cross-Platform Build Instructions

You can distribute the entire CAMO infrastructure as a standalone executable avoiding any virtual environment constraints natively via PyInstaller or Nuitka.

### Windows (.exe)
```bash
pip install pyinstaller
pyinstaller --name "CAMO_Controller" --onefile main.py --hidden-import="uvicorn.logging" --hidden-import="uvicorn.loops" --hidden-import="uvicorn.loops.auto" --hidden-import="uvicorn.protocols" --hidden-import="uvicorn.protocols.http" --hidden-import="uvicorn.protocols.http.auto" --hidden-import="uvicorn.websockets" --hidden-import="uvicorn.websockets.auto" --hidden-import="uvicorn.lifespan" --hidden-import="uvicorn.lifespan.on"
```

### Linux Package
```bash
pip install nuitka
python -m nuitka --standalone --onefile --output-dir=build main.py
```

### macOS Application
```bash
pip install pyinstaller
pyinstaller --name "CAMO_Controller" --windowed --onefile main.py
```
