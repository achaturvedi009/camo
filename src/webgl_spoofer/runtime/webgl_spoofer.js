(function(fp) {
    if (!window.WebGLRenderingContext) return;

    const paramMap = window.__CAMO_GPU_MAPPER(fp);
    const applyNoise = window.__CAMO_WEBGL_NOISE(fp.rendering ? fp.rendering.webglHash : "seed");

    const extensions = (fp.rendering && fp.rendering.webgl && fp.rendering.webgl.supported_extensions)
        ? fp.rendering.webgl.supported_extensions
        : ["OES_texture_float", "WEBGL_debug_renderer_info", "EXT_texture_filter_anisotropic", "WEBGL_depth_texture"];

    const overrideContext = (ContextObj) => {
        if (!ContextObj || !ContextObj.prototype) return;
        const proto = ContextObj.prototype;

        // 1. getParameter
        const originalGetParameter = proto.getParameter;
        const spoofedGetParameter = function getParameter(parameter) {
            if (paramMap.hasOwnProperty(parameter)) {
                return paramMap[parameter];
            }
            return originalGetParameter.call(this, parameter);
        };
        spoofedGetParameter.toString = () => "function getParameter() { [native code] }";
        Object.defineProperty(proto, 'getParameter', { value: spoofedGetParameter, writable: true, enumerable: true, configurable: true });

        // 2. getSupportedExtensions
        const originalGetSupportedExtensions = proto.getSupportedExtensions;
        const spoofedGetSupportedExtensions = function getSupportedExtensions() {
            // Usually we return the array based on fingerprint
            // But we must also ensure WEBGL_debug_renderer_info is present if requested
            return extensions;
        };
        spoofedGetSupportedExtensions.toString = () => "function getSupportedExtensions() { [native code] }";
        Object.defineProperty(proto, 'getSupportedExtensions', { value: spoofedGetSupportedExtensions, writable: true, enumerable: true, configurable: true });

        // 3. getExtension
        const originalGetExtension = proto.getExtension;
        const spoofedGetExtension = function getExtension(name) {
            // Check if extension is mocked or block it if not in list
            if (!extensions.includes(name) && name !== "WEBGL_debug_renderer_info") {
                return null;
            }
            return originalGetExtension.call(this, name);
        };
        spoofedGetExtension.toString = () => "function getExtension() { [native code] }";
        Object.defineProperty(proto, 'getExtension', { value: spoofedGetExtension, writable: true, enumerable: true, configurable: true });

        // 4. getShaderPrecisionFormat
        const originalGetShaderPrecisionFormat = proto.getShaderPrecisionFormat;
        const precisionMap = {
            "highp": { rangeMin: 127, rangeMax: 127, precision: 23 },
            "mediump": { rangeMin: 63, rangeMax: 63, precision: 10 },
            "lowp": { rangeMin: 31, rangeMax: 31, precision: 8 }
        };
        const spoofedGetShaderPrecisionFormat = function getShaderPrecisionFormat(shaderType, precisionType) {
            // Mock precision based on config
            const expectedPrecision = (fp.rendering && fp.rendering.webgl) ? fp.rendering.webgl.shader_precision : "highp";
            const nativeResult = originalGetShaderPrecisionFormat.call(this, shaderType, precisionType);

            // Very roughly mapping logic
            if (nativeResult && precisionMap[expectedPrecision]) {
                const mocked = Object.create(WebGLShaderPrecisionFormat.prototype);
                // Cannot overwrite readonly without Object.defineProperty? Wait, WebGLShaderPrecisionFormat properties are readonly.
                // We can just construct a mock object that duck types correctly.
                Object.defineProperty(mocked, 'rangeMin', { value: precisionMap[expectedPrecision].rangeMin, enumerable: true });
                Object.defineProperty(mocked, 'rangeMax', { value: precisionMap[expectedPrecision].rangeMax, enumerable: true });
                Object.defineProperty(mocked, 'precision', { value: precisionMap[expectedPrecision].precision, enumerable: true });
                return mocked;
            }
            return nativeResult;
        };
        spoofedGetShaderPrecisionFormat.toString = () => "function getShaderPrecisionFormat() { [native code] }";
        Object.defineProperty(proto, 'getShaderPrecisionFormat', { value: spoofedGetShaderPrecisionFormat, writable: true, enumerable: true, configurable: true });

        // 5. readPixels (Rendering Noise)
        const originalReadPixels = proto.readPixels;
        const spoofedReadPixels = function readPixels(...args) {
            originalReadPixels.apply(this, args);
            // args[6] is the pixels array, args[2] is width, args[3] is height
            if (args.length >= 7 && args[6]) {
                applyNoise(args[6], args[2], args[3]);
            }
        };
        spoofedReadPixels.toString = () => "function readPixels() { [native code] }";
        Object.defineProperty(proto, 'readPixels', { value: spoofedReadPixels, writable: true, enumerable: true, configurable: true });
    };

    overrideContext(window.WebGLRenderingContext);
    overrideContext(window.WebGL2RenderingContext);

})(window.__CAMO_FP__);
