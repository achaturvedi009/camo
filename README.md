# CAMO Antidetect Browser

A lightweight, login-free, enterprise-grade anti-detect browser platform utilizing a hardened Camoufox core engine. CAMO supports unlimited, isolated browser profiles complete with cryptographically deterministic device fingerprints, dynamic JS runtime spoofing, fully mocked Chrome environments, and local SQLite data isolation.

It is specifically architected to bypass advanced bot detection mechanisms such as Pixelscan, Cloudflare Bot Management, FingerprintJS, DataDome, PerimeterX, and Kasada.

---

## 🌟 Next-Generation Features

- **Multi-Profile Management**: Create, edit, clone, and delete isolated profiles effortlessly via the clean local UI, without any login limitations.
- **Deterministic Fingerprint Engine**: Our ultra-fast (`<10ms`) core automatically generates valid, logically consistent, layered browser fingerprints (User-Agent, Canvas, WebGL, AudioContext, Network, Hardware, TLS) based on OS presets (Windows, Linux, Android) using SHA-256 seeding.
- **Enterprise Runtime JS Spoofing**: Injects a hardened emulation layer via the Chrome DevTools Protocol (`add_init_script`) directly into the Playwright context *before* any page JavaScript runs. Overrides `navigator`, `screen`, `canvas`, `webrtc`, and hardware specs gracefully while masking function signatures with `[native code]` patches.
- **Chrome Environment Emulation**: Fools invasive detections looking for real user profiles by mocking legacy extension and Chrome app scopes (`window.chrome.runtime`, `app`, `webstore`, `csi`, `loadTimes`).
- **Timezone GeoIP Routing**: Automatically links the requested proxy IP with matching local Timezones, drastically reducing behavioral anomalies.
- **Camoufox Version Manager**: Integrates with the Python `packaging` framework to cleanly fetch, isolate, and install multiple underlying browser versions directly from PyPI.
- **Local-First Storage**: Uses SQLAlchemy atop an SQLite database (`data/profiles.db`). Zero telemetry, zero accounts, zero cloud dependencies.

---

## 🏗 Architecture Layers

- **Backend API**: Local FastAPI / Uvicorn server handling all proxy, database, and process bridging.
- **Core Orchestrator**: Manages parallel isolated `BrowserContext` instances.
- **Fingerprint Engine (`src/fingerprint_engine/`)**: Datasets, builders, and validators for 10 levels of device modeling.
- **Runtime Emulation (`src/runtime_spoofer/` & `src/chrome_emulation/`)**: Bundled JavaScript artifacts maintaining object prototype validity under adversarial inspection.
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
- `src/ui/`: The dashboard GUI logic.
