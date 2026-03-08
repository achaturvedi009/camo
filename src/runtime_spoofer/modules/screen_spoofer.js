(function(fp) {
    const [w, h] = fp.screen.split('x').map(Number);
    const dpr = fp.devicePixelRatio || 1;

    Object.defineProperty(window, 'devicePixelRatio', { get: () => dpr });
    Object.defineProperty(screen, 'width', { get: () => w });
    Object.defineProperty(screen, 'height', { get: () => h });
    Object.defineProperty(screen, 'availWidth', { get: () => w });
    Object.defineProperty(screen, 'availHeight', { get: () => h });
    Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
    Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
})(window.__CAMO_FP__);
