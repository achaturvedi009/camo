(function(fp) {
    if (!window.HTMLCanvasElement || !window.CanvasRenderingContext2D) return;

    const seed = fp.canvasHash || "default_seed";
    const applyNoise = window.__CAMO_NOISE_ENGINE.applyNoise;

    // 1. getImageData
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    const spoofedGetImageData = function getImageData(...args) {
        const imageData = originalGetImageData.apply(this, args);
        return applyNoise(imageData, seed);
    };
    spoofedGetImageData.toString = () => "function getImageData() { [native code] }";
    Object.defineProperty(CanvasRenderingContext2D.prototype, 'getImageData', {
        value: spoofedGetImageData,
        writable: true,
        enumerable: true,
        configurable: true
    });

    // 2. toDataURL
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const spoofedToDataURL = function toDataURL(...args) {
        const ctx = this.getContext('2d');
        if (ctx) {
            const width = this.width;
            const height = this.height;
            if (width > 0 && height > 0) {
                const imageData = originalGetImageData.call(ctx, 0, 0, width, height);
                const noisedData = applyNoise(imageData, seed);
                ctx.putImageData(noisedData, 0, 0);
            }
        }
        return originalToDataURL.apply(this, args);
    };
    spoofedToDataURL.toString = () => "function toDataURL() { [native code] }";
    Object.defineProperty(HTMLCanvasElement.prototype, 'toDataURL', {
        value: spoofedToDataURL,
        writable: true,
        enumerable: true,
        configurable: true
    });

    // 3. toBlob
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;
    const spoofedToBlob = function toBlob(callback, type, quality) {
        const ctx = this.getContext('2d');
        if (ctx) {
            const width = this.width;
            const height = this.height;
            if (width > 0 && height > 0) {
                const imageData = originalGetImageData.call(ctx, 0, 0, width, height);
                const noisedData = applyNoise(imageData, seed);
                ctx.putImageData(noisedData, 0, 0);
            }
        }
        return originalToBlob.call(this, callback, type, quality);
    };
    spoofedToBlob.toString = () => "function toBlob() { [native code] }";
    Object.defineProperty(HTMLCanvasElement.prototype, 'toBlob', {
        value: spoofedToBlob,
        writable: true,
        enumerable: true,
        configurable: true
    });
})(window.__CAMO_FP__);
