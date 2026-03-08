(function(fp) {
    const vendor = fp.gpuVendor;
    const renderer = fp.gpuRenderer;

    const overrideWebGL = (contextName) => {
        const proto = window[contextName]?.prototype;
        if (!proto) return;

        const originalGetParameter = proto.getParameter;
        proto.getParameter = function(parameter) {
            // UNMASKED_VENDOR_WEBGL
            if (parameter === 37445) return vendor;
            // UNMASKED_RENDERER_WEBGL
            if (parameter === 37446) return renderer;
            return originalGetParameter.call(this, parameter);
        };
        proto.getParameter.toString = () => "function getParameter() { [native code] }";
    };

    overrideWebGL('WebGLRenderingContext');
    overrideWebGL('WebGL2RenderingContext');
})(window.__CAMO_FP__);
