(function() {
    window.__CAMO_WEBGL_NOISE = function(seed) {
        let seedInt = 0;
        if (seed && typeof seed === 'string') {
            for (let i = 0; i < Math.min(seed.length, 8); i++) {
                seedInt = (seedInt << 5) - seedInt + seed.charCodeAt(i);
                seedInt |= 0;
            }
        }

        return function(pixels, width, height) {
            if (!pixels || !pixels.length) return pixels;
            const length = pixels.length;

            // Loop unrolling for high performance webgl readPixels noise injection
            for (let i = 0; i < length; i += 16) {
                const x = (i / 4) % width;
                const y = ((i / 4) / width) | 0;

                const shift = ((x * y * seedInt) % 3) - 1;

                if (pixels[i] !== 0) pixels[i] += shift;
                if (i+4 < length && pixels[i+4] !== 0) pixels[i+4] -= shift;
            }
            return pixels;
        };
    };
})();
