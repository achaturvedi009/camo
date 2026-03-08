# CAMO Antidetect Browser

A lightweight, login-free, enterprise-grade anti-detect browser platform utilizing a hardened Camoufox core engine. CAMO supports unlimited, isolated browser profiles complete with cryptographically deterministic device fingerprints, dynamic JS runtime spoofing, fully mocked Chrome environments, and local SQLite data isolation.

It is specifically architected to bypass advanced bot detection mechanisms such as Pixelscan, Cloudflare Bot Management, FingerprintJS, DataDome, PerimeterX, and Kasada.

---

## 🌟 Next-Generation Features

- **Multi-Profile Management**: Create, edit, clone, and delete isolated profiles effortlessly via the clean local UI, without any login limitations.
- **Deterministic Fingerprint Engine**: Our ultra-fast (`<10ms`) core automatically generates valid, logically consistent, layered browser fingerprints (User-Agent, Canvas, WebGL, AudioContext, Network, Hardware, TLS) based on OS presets (Windows, Linux, Android) using SHA-256 seeding.
- **Enterprise Runtime JS Spoofing**: Injects a hardened emulation layer via the Chrome DevTools Protocol (`add_init_script`) directly into the Playwright context *before* any page JavaScript runs. Overrides `navigator`, `screen`, `canvas`, `webrtc`, and hardware specs gracefully while masking function signatures with `[native code]` patches.
- **Advanced Canvas Fingerprint Spoofing**: A dedicated enterprise pixel-noise rendering layer. Intercepts `toDataURL`, `toBlob`, and `getImageData`, silently shuffling pixel entropy perfectly tied to your profile ID, evading FingerprintJS canvas tracking schemas `< 1ms` speed overhead.
- **Enterprise WebGL Spoofing**: An advanced deterministic GPU emulation layer mocking underlying hardware `VENDOR` and `RENDERER` profiles. Mocks maximum texture limits, exact anisotropic filtering extensions natively matching Windows/Mac/Linux GPU datasets, alongside randomized `readPixels` noise.
- **AudioContext Fingerprint Emulation**: Injects micro-deterministic noise across native `AudioBuffer` and `AnalyserNode` components safely. Validates `startRendering` buffer returns modifying frequency hashes implicitly while neutralizing detection logic entirely.
- **Enterprise Font Emulation**: Hides physical system font fingerprints mapping strictly isolated OS fonts (`fonts_windows.json`, `fonts_macos.json`). Defeats FontFace bounding-box metric comparisons flawlessly using Canvas TextMetrics intercepting logic and generic font overrides natively mapping into rendering properties.
- **Chrome Environment Emulation**: Fools invasive detections looking for real user profiles by mocking legacy extension and Chrome app scopes (`window.chrome.runtime`, `app`, `webstore`, `csi`, `loadTimes`).
- **Permissions API Emulation**: Provides an extremely accurate stealth implementation of `navigator.permissions.query()`. It maps OS-level fingerprint markers into appropriate `PermissionStatus` promise resolutions while preserving `toString()` and property prototype integrity to spoof bot defense queries.
- **Timezone GeoIP Routing**: Automatically links the requested proxy IP with matching local Timezones, drastically reducing behavioral anomalies.
- **Camoufox Version Manager**: Integrates with the Python `packaging` framework to cleanly fetch, isolate, and install multiple underlying browser versions directly from PyPI.
- **Local-First Storage**: Uses SQLAlchemy atop an SQLite database (`data/profiles.db`). Zero telemetry, zero accounts, zero cloud dependencies.

---

## 🏗 Architecture Layers

- **Backend API**: Local FastAPI / Uvicorn server handling all proxy, database, and process bridging.
- **Core Orchestrator**: Manages parallel isolated `BrowserContext` instances.
- **Fingerprint Engine (`src/fingerprint_engine/`)**: Datasets, builders, and validators for 10 levels of device modeling.
- **Runtime Emulation (`src/runtime_spoofer/`, `src/chrome_emulation/`, `src/permissions_spoofer/`, `src/canvas_spoofer/`, `src/webgl_spoofer/`, `src/audio_spoofer/`, `src/font_spoofer/`)**: Bundled JavaScript artifacts maintaining object prototype validity under adversarial inspection.
- **Frontend App**: Responsive Vue.js + Tailwind CSS local UI wrapper.

---

## 🚀 Installation & Setup

1. **Clone the Repository** and navigate into the folder.
2. **Create a Virtual Environment** and install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Browser Binaries (Playwright System Dependencies)**:
   ```bash
   playwright install-deps
   ```

---

## 💻 Usage

1. **Start the Controller Backend:**
   ```bash
   python main.py
   ```
   *(Alternatively: `uvicorn src.api.main:app --host 127.0.0.1 --port 8000`)*

2. **Open the Control Panel UI:**
   Open `src/ui/index.html` in any standard web browser (Chrome, Firefox, Safari).

3. **Launch Profiles:**
   Create a new profile (or clone an existing one), attach your desired Proxy details, preview the deterministic hardware fingerprint, and click **Start**.

---

## 📦 Building Standalone Executables

If you wish to distribute the CAMO Backend without requiring local Python environments, use PyInstaller.

```bash
pip install pyinstaller
pyinstaller --name "CAMO_Controller" --onefile main.py
```
*Run the resulting executable generated inside the `dist/` directory.*

---

## 🛠 Troubleshooting

- **Target closed / X11 Error (Linux)**: If a profile crashes upon start, your Linux machine may lack an active display server (e.g., inside Docker or a headless VPS). The app will automatically try to initialize `headless="virtual"`. Ensure `Xvfb` is installed via your OS package manager (`apt-get install xvfb`).
- **Dependencies Missing**: If you encounter Pydantic or ModuleNotFound errors, simply re-run `pip install -r requirements.txt`.

---

## 📁 Repository Structure
- `data/`: Contains isolated `profiles.db` SQLite storage. (Ignored from version control).
- `src/api/`: Main FastAPI router and endpoints.
- `src/core/`: Database models, profile orchestrator, proxy validation.
- `src/fingerprint_engine/`: Logic parsing JSON hardware sets into SHA-256 mapped characteristics.
- `src/runtime_spoofer/`: Overrides core browser prototypes safely.
- `src/chrome_emulation/`: Replicates `window.chrome` components precisely.
- `src/permissions_spoofer/`: Masks `navigator.permissions` properties perfectly mapping rules to the current OS spoofing layer.
- `src/canvas_spoofer/`: Modifies rendering canvas pixels to generate consistent profile-level cryptographic spoofing hashes.
- `src/webgl_spoofer/`: Modifies GPU profiles and parameters rendering realistic hardware configurations safely against Kasada / DataDome.
- `src/audio_spoofer/`: Hooks `AnalyserNode` and offline rendering outputs shifting floating arrays resolving DataDome hash queries flawlessly.
- `src/font_spoofer/`: Masks system fonts replacing TextMetrics results dynamically preventing CSS FontFace inspection attacks globally.
- `src/ui/`: The dashboard GUI logic.
