(function() {
    window.__CAMO_NOISE_ENGINE = {
        applyNoise: function(imageData, seed) {
            if (!imageData || !imageData.data) return imageData;

            let seedInt = 0;
            if (seed && typeof seed === 'string') {
                for (let i = 0; i < Math.min(seed.length, 8); i++) {
                    seedInt = (seedInt << 5) - seedInt + seed.charCodeAt(i);
                    seedInt |= 0;
                }
            }

            const data = imageData.data;
            const length = data.length;
            const w = imageData.width;

            // Loop unrolling for extreme performance
            for (let i = 0; i < length; i += 16) {
                const x = (i / 4) % w;
                const y = ((i / 4) / w) | 0;

                const shift = ((x * y * seedInt) % 3) - 1;

                if (data[i] !== 0) {
                    data[i] = data[i] + shift;
                }
                if (i+4 < length && data[i+4] !== 0) {
                    data[i+4] = data[i+4] - shift;
                }
            }

            return imageData;
        }
    };
})();
