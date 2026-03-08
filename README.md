# CAMO Enterprise Antidetect Browser Platform

A lightweight, login-free, scalable enterprise-grade anti-detect browser platform utilizing a hardened Camoufox core engine. CAMO supports thousands of concurrent, isolated browser profiles completely masked with cryptographically deterministic device fingerprints, dynamic JS runtime spoofing, fully mocked Chrome environments, native media proxies, and isolated local SQLite architectures natively.

It is specifically architected to bypass advanced bot detection mechanisms such as Pixelscan, Cloudflare Bot Management, FingerprintJS, DataDome, PerimeterX, Kasada, and AmiUnique.

---

## 🌟 Enterprise Features Matrix

- **Multi-Profile Database Management**: Run thousands of distinct isolated profiles utilizing SQLAlchemy bounding over SQLite (`data/profiles.db`).
- **Cryptographic Fingerprint Engine**: Ultra-fast `<10ms` core generating valid, logically consistent, layered hardware configurations based off profile SHA-256 seeding preventing regression collisions cleanly.
- **Enterprise Runtime JS Spoofing**: Injects a hardened emulation layer via Playwright's `add_init_script`. Modifies generic navigator properties natively retaining `[native code]` `.toString()` validations.
- **Advanced Canvas & WebGL Emulation**: Dedicated pixel-noise rendering engines dynamically shifting pixel bounds synchronously circumventing exact hash limits mapping perfectly over `UNMASKED_RENDERER` restrictions locally.
- **AudioContext Spoofing**: Wraps native `AudioBuffer` and `OfflineAudioContext` pipelines protecting analysis routines utilizing native offset arrays dynamically.
- **Enterprise Font Emulation**: Maps perfectly localized bounding boxes bypassing precise CSS FontFace scaling tricks via TextMetrics injection limits mapping exactly to the chosen OS class correctly.
- **WebRTC & Network Protections**: Defeats STUN/TURN proxy leaks directly via parsing asynchronous local IP blocks bridging only valid explicit assigned proxy paths globally blocking localized footprint discovery algorithms natively.
- **Media Devices Generator**: Masks native driver outputs wrapping `navigator.mediaDevices.enumerateDevices()` strictly matching internal profile hashing identifiers predictably across restarts correctly avoiding dynamic mapping bugs completely.
- **Automated Validation Core**: Evaluates UA mismatches, graphic OS mapping disparities natively resolving strict validation checks before execution safely natively.
- **Integrated Diagnostics UI**: Evaluates hardware spoof metrics visually via a local unified tracking dashboard booted securely mapping proxy health boundaries clearly on startup natively mapped efficiently.
- **Timezone GeoIP Routing**: Reconciles public IP inputs inherently assigning the accurate UTC offset arrays explicitly masking mismatched browser timing metrics successfully natively via external parsing routes natively.

---

## 🏗 Subsystem Layout

- **`src/api/`**: Main backend endpoints mapping UI boundaries to Playwright states correctly.
- **`src/core/`**: Lower-layer orchestrators (Database Models, Processes).
- **`src/fingerprint_engine/`**: The deterministic JSON hardware generator core.
- **`src/runtime_spoofer/`**: Generalized Javascript `navigator` / JS API interceptors.
- **`src/chrome_emulation/`**: Accurate `window.chrome.app` & `runtime` simulators masking headless boundaries tightly.
- **`src/permissions_spoofer/`**: Promisified `.query()` maskers strictly tracking deterministic arrays precisely.
- **`src/canvas_spoofer/`**: Low-level pixel manipulation and `toDataUrl` injection limits safely.
- **`src/webgl_spoofer/`**: High-performance graphics extension manipulation overrides seamlessly.
- **`src/audio_spoofer/`**: Floating array manipulations preventing generic hardware correlations accurately.
- **`src/font_spoofer/`**: Measurement bounds preventing standard CSS bounding probes seamlessly.
- **`src/webrtc_protector/`**: Subnet IP parsing arrays avoiding leak parameters correctly reliably.
- **`src/camo/`**: The Enterprise configuration backend isolating user-directories (`profiles/`), checking fingerprint metrics (`security/`), generating media definitions (`runtime/`), managing localized proxy states (`network/`), handling dashboard analytics natively (`dashboard/`), and integrating engines successfully (`browser_engines/`).

---

## 🚀 Installation & Setup

1. **Clone the Repository** and navigate into the folder.
2. **Create a Virtual Environment** and install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Browser Binaries (Playwright Dependencies)**:
   ```bash
   playwright install-deps
   ```

---

## 💻 Usage

1. **Start the Controller Backend:**
   ```bash
   python main.py
   ```

2. **Open the Control Panel UI:**
   Open `src/ui/index.html` in any standard web browser (Chrome, Firefox, Safari).

3. **Launch Profiles:**
   Hit start on any assigned profiles and CAMO will orchestrate the database layers launching isolated binaries perfectly protected immediately routing into the diagnostic startup dashboard automatically correctly mapping validations visually successfully.

---

## 📦 Building Standalone Executables

If you wish to distribute the CAMO Backend natively.
```bash
pip install pyinstaller
pyinstaller --name "CAMO_Controller" --onefile main.py
```
*Run the resulting executable generated inside the `dist/` directory.*
