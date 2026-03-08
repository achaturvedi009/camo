(function(fp) {
    if (!fp || !fp.hardware) return;

    let screenW = 1920;
    let screenH = 1080;
    if (fp.hardware.screen_resolution) {
        const parts = fp.hardware.screen_resolution.split('x');
        if (parts.length === 2) {
            screenW = parseInt(parts[0], 10) || 1920;
            screenH = parseInt(parts[1], 10) || 1080;
        }
    }
    const dpr = fp.hardware.devicePixelRatio || 1;

    // Cache initial outer bounds to prevent dynamic resizing fingerprint leaks
    // By locking initial spoof values, resizing the physical window doesn't change the logical fingerprint
    const initialOuterWidth = Math.min(window.outerWidth || screenW, screenW);
    const initialOuterHeight = Math.min(window.outerHeight || screenH, screenH);

    const chromeX = 16;
    const chromeY = 85;

    const spoofedOuterWidth = function outerWidth() { return initialOuterWidth; };
    spoofedOuterWidth.toString = () => "function get outerWidth() { [native code] }";
    Object.defineProperty(window, 'outerWidth', { get: spoofedOuterWidth, enumerable: true, configurable: true });

    const spoofedOuterHeight = function outerHeight() { return initialOuterHeight; };
    spoofedOuterHeight.toString = () => "function get outerHeight() { [native code] }";
    Object.defineProperty(window, 'outerHeight', { get: spoofedOuterHeight, enumerable: true, configurable: true });

    const spoofedInnerWidth = function innerWidth() { return Math.max(0, initialOuterWidth - chromeX); };
    spoofedInnerWidth.toString = () => "function get innerWidth() { [native code] }";
    Object.defineProperty(window, 'innerWidth', { get: spoofedInnerWidth, enumerable: true, configurable: true });

    const spoofedInnerHeight = function innerHeight() { return Math.max(0, initialOuterHeight - chromeY); };
    spoofedInnerHeight.toString = () => "function get innerHeight() { [native code] }";
    Object.defineProperty(window, 'innerHeight', { get: spoofedInnerHeight, enumerable: true, configurable: true });

    const spoofedDpr = function devicePixelRatio() { return dpr; };
    spoofedDpr.toString = () => "function get devicePixelRatio() { [native code] }";
    Object.defineProperty(window, 'devicePixelRatio', { get: spoofedDpr, enumerable: true, configurable: true });

    // Lock event propagation on resize if queried by scripts for width checks
    window.addEventListener('resize', (e) => {
        e.stopImmediatePropagation();
    }, true);

})(window.__CAMO_FP__);
