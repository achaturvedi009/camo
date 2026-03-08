(function(fp) {
    if (!fp || !fp.hardware) return;

    let screenW = 1920;
    let screenH = 1080;
    let colorDepth = fp.hardware.color_depth || 24;

    if (fp.hardware.screen_resolution) {
        const parts = fp.hardware.screen_resolution.split('x');
        if (parts.length === 2) {
            screenW = parseInt(parts[0], 10) || 1920;
            screenH = parseInt(parts[1], 10) || 1080;
        }
    }

    // Avail is usually screen - taskbar (approx 40px on windows)
    const availH = screenH > 40 ? screenH - 40 : screenH;

    const defineScreenProp = (propName, value) => {
        const spoofed = function() { return value; };
        spoofed.toString = () => `function get ${propName}() { [native code] }`;
        Object.defineProperty(window.screen, propName, {
            get: spoofed,
            enumerable: true,
            configurable: true
        });
    };

    defineScreenProp('width', screenW);
    defineScreenProp('height', screenH);
    defineScreenProp('availWidth', screenW);
    defineScreenProp('availHeight', availH);
    defineScreenProp('colorDepth', colorDepth);
    defineScreenProp('pixelDepth', colorDepth);

})(window.__CAMO_FP__);
