# Enterprise WebGL Spoofing Layer

The WebGL Environment Emulation Layer intercepts core `WebGLRenderingContext` and `WebGL2RenderingContext` getters across `<canvas>` nodes, overriding parameters mapped directly from realistic CAMO backend hashes.

## Handled Signatures:
- UNMASKED_VENDOR_WEBGL
- UNMASKED_RENDERER_WEBGL
- MAX_TEXTURE_SIZE & MAX_RENDERBUFFER_SIZE limits
- `getShaderPrecisionFormat()`
- `getSupportedExtensions()` / `getExtension()` limits
- Deterministic readPixels visual hashing noise via `render_noise_engine.js`.

These APIs are explicitly safeguarded behind proxy function descriptor wrappers masking via `.toString()`.
