(function(fp) {
    const fonts = fp.environment && fp.environment.fonts ? fp.environment.fonts : [];
    const engine = window.__CAMO_FONT_ENGINE(fonts);

    // 1. Override Canvas Text Measurement
    if (window.CanvasRenderingContext2D) {
        const originalMeasureText = CanvasRenderingContext2D.prototype.measureText;
        const spoofedMeasureText = function measureText(text) {
            const metrics = originalMeasureText.call(this, text);
            // Current font is stored in this.font
            const isAvailable = engine.isValidFont(this.font);

            // We cannot just mutate TextMetrics easily as it's a native object with readonly properties.
            // We must create a mock object inheriting its prototype.
            const mockMetrics = Object.create(TextMetrics.prototype);

            // List of properties to potentially proxy
            const props = ['width', 'actualBoundingBoxLeft', 'actualBoundingBoxRight',
                           'actualBoundingBoxAscent', 'actualBoundingBoxDescent',
                           'fontBoundingBoxAscent', 'fontBoundingBoxDescent'];

            for (let i=0; i<props.length; i++) {
                const prop = props[i];
                if (prop in metrics) {
                    Object.defineProperty(mockMetrics, prop, {
                        value: prop === 'width' || prop.includes('Right')
                               ? engine.shiftMetrics(metrics[prop], isAvailable)
                               : metrics[prop],
                        enumerable: true
                    });
                }
            }
            return mockMetrics;
        };
        spoofedMeasureText.toString = () => "function measureText() { [native code] }";
        Object.defineProperty(CanvasRenderingContext2D.prototype, 'measureText', {
            value: spoofedMeasureText, writable: true, enumerable: true, configurable: true
        });
    }

    // 2. Override Document Fonts (FontFaceSet)
    if (document.fonts) {
        const originalCheck = document.fonts.check;
        const spoofedCheck = function check(font, text) {
            // "12px 'Arial'" -> Extract 'Arial'
            let family = "";
            const match = font.match(/['"]?([^'"]+)['"]?/);
            if (match) {
                family = match[1];
            }
            // If it's valid in our subset, return original check (which might be true if installed natively)
            // Wait, if it's not installed natively but IS in our subset, we should force true?
            // Actually, we only block fonts that are NOT in our subset but might be installed natively.
            // For anti-detect, if a font is natively installed but we want to HIDE it, we return false.
            if (!engine.isValidFont(family)) {
                return false;
            }

            // If it IS in our subset, but the host doesn't have it... this is trickier.
            // Usually, anti-detect limits your fonts to the lowest common denominator, or injects web fonts.
            // We'll let the native engine resolve it, but at least we block hidden ones.
            return originalCheck.call(this, font, text);
        };
        spoofedCheck.toString = () => "function check() { [native code] }";
        Object.defineProperty(document.fonts.constructor.prototype, 'check', {
            value: spoofedCheck, writable: true, enumerable: true, configurable: true
        });
    }
})(window.__CAMO_FP__);
