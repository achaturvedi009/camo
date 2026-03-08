(function() {
    window.__CAMO_GPU_MAPPER = function(fp) {
        if (!fp || !fp.rendering || !fp.rendering.webgl) return {};

        const webglInfo = fp.rendering.webgl;

        // Define standard GL constants mappings
        return {
            // UNMASKED_VENDOR_WEBGL
            37445: webglInfo.vendor || "Google Inc. (Intel)",
            // UNMASKED_RENDERER_WEBGL
            37446: webglInfo.renderer || "ANGLE (Intel, Intel(R) UHD Graphics 620, OpenGL 4.6)",
            // MAX_TEXTURE_SIZE
            3379: webglInfo.max_texture_size || 8192,
            // MAX_RENDERBUFFER_SIZE
            34024: webglInfo.max_texture_size || 8192, // Usually matches texture size
            // MAX_CUBE_MAP_TEXTURE_SIZE
            34076: (webglInfo.max_texture_size || 8192) / 2,
            // MAX_VERTEX_ATTRIBS
            34921: 16,
            // MAX_VERTEX_UNIFORM_VECTORS
            36347: 4096,
            // MAX_FRAGMENT_UNIFORM_VECTORS
            36349: 1024,
            // MAX_TEXTURE_IMAGE_UNITS
            34930: 16,
            // MAX_VERTEX_TEXTURE_IMAGE_UNITS
            35660: 16
        };
    };
})();
