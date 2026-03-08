(function(fp) {
    const hashStr = fp.canvasHash;
    const injectNoise = (ctx) => {
        const shift = hashStr.charCodeAt(0) % 10;
        ctx.fillStyle = `rgba(255,255,255,${shift / 1000})`;
        ctx.fillRect(0, 0, 1, 1);
    };

    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(...args) {
        const ctx = this.getContext('2d');
        if (ctx) injectNoise(ctx);
        return originalToDataURL.apply(this, args);
    };
    HTMLCanvasElement.prototype.toDataURL.toString = () => "function toDataURL() { [native code] }";

    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    CanvasRenderingContext2D.prototype.getImageData = function(...args) {
        injectNoise(this);
        return originalGetImageData.apply(this, args);
    };
    CanvasRenderingContext2D.prototype.getImageData.toString = () => "function getImageData() { [native code] }";
})(window.__CAMO_FP__);
