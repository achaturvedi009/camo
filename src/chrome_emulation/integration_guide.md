# Chrome Environment Emulation Layer

The Chrome Environment Emulation Layer is a subsystem of the CAMO anti-detect browser project. It perfectly replicates the internal `window.chrome` APIs expected by bot detection scripts.

## How it works

When a browser worker (`src/core/browser_worker.py`) starts up with a fingerprint claiming to be "Chrome", it utilizes the `add_init_script` Playwright command to inject this emulation code.

The injection script is bundled from the `modules` directory:
- `chrome_object.js`: Instantiates `window.chrome` securely.
- `app_module.js`: Emulates `chrome.app` behavior and permissions states.
- `runtime_module.js`: Emulates `chrome.runtime` connections, mimicking empty extensions contexts.
- `webstore_module.js`: Emulates legacy `chrome.webstore` properties.
- `csi_module.js`: Provides realistic `chrome.csi()` page load metrics.
- `loadtimes_module.js`: Provides `chrome.loadTimes()` realistic legacy DOM load metrics.

## Evasion Details

To evade deep inspection, every single method in the emulated API masks its signature via patched `toString()` properties.

Example:
Calling `chrome.csi.toString()` natively in a standard JS execution context returns `function csi() { [native code] }` identically matching an actual Chrome environment.

This happens in less than `<10ms` natively handled by Playwright via Chrome DevTools Protocol (`CDP`).
