(function(fp) {
    if (!fp || !fp.hardware) return;

    // Safely extract screen dimensions
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

    // Outer Width/Height: bounded by physical screen limits
    const clampOuter = (val, max) => Math.min(Math.max(val, 0), max);

    // Inner Width/Height: realistically inner <= outer
    // The browser usually has chrome (address bar, scrollbars) reducing inner bounds.
    const chromeX = 16;  // Scrollbar width
    const chromeY = 85;  // Address bar + tabs

    // Original Getters
    const getOuterWidth = Object.getOwnPropertyDescriptor(window, 'outerWidth').get;
    const getOuterHeight = Object.getOwnPropertyDescriptor(window, 'outerHeight').get;
    const getInnerWidth = Object.getOwnPropertyDescriptor(window, 'innerWidth').get;
    const getInnerHeight = Object.getOwnPropertyDescriptor(window, 'innerHeight').get;

    // Wrap Outer Width
    const spoofedOuterWidth = function outerWidth() {
        try {
            const nativeOuter = getOuterWidth.call(this);
            return clampOuter(nativeOuter, screenW);
        } catch(e) { return screenW; }
    };
    spoofedOuterWidth.toString = () => "function get outerWidth() { [native code] }";
    Object.defineProperty(window, 'outerWidth', { get: spoofedOuterWidth, enumerable: true, configurable: true });

    // Wrap Outer Height
    const spoofedOuterHeight = function outerHeight() {
        try {
            const nativeOuter = getOuterHeight.call(this);
            return clampOuter(nativeOuter, screenH);
        } catch(e) { return screenH; }
    };
    spoofedOuterHeight.toString = () => "function get outerHeight() { [native code] }";
    Object.defineProperty(window, 'outerHeight', { get: spoofedOuterHeight, enumerable: true, configurable: true });

    // Wrap Inner Width
    const spoofedInnerWidth = function innerWidth() {
        try {
            const nativeOuter = spoofedOuterWidth.call(this);
            const nativeInner = getInnerWidth.call(this);
            return Math.min(nativeInner, nativeOuter - chromeX);
        } catch(e) { return screenW - chromeX; }
    };
    spoofedInnerWidth.toString = () => "function get innerWidth() { [native code] }";
    Object.defineProperty(window, 'innerWidth', { get: spoofedInnerWidth, enumerable: true, configurable: true });

    // Wrap Inner Height
    const spoofedInnerHeight = function innerHeight() {
        try {
            const nativeOuter = spoofedOuterHeight.call(this);
            const nativeInner = getInnerHeight.call(this);
            return Math.min(nativeInner, nativeOuter - chromeY);
        } catch(e) { return screenH - chromeY; }
    };
    spoofedInnerHeight.toString = () => "function get innerHeight() { [native code] }";
    Object.defineProperty(window, 'innerHeight', { get: spoofedInnerHeight, enumerable: true, configurable: true });

    // Device Pixel Ratio
    const spoofedDpr = function devicePixelRatio() { return dpr; };
    spoofedDpr.toString = () => "function get devicePixelRatio() { [native code] }";
    Object.defineProperty(window, 'devicePixelRatio', { get: spoofedDpr, enumerable: true, configurable: true });

})(window.__CAMO_FP__);
