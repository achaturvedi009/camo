(function() {
    window.__CAMO_AUDIO_NOISE = function(seedStr) {
        let seedInt = 0;
        if (seedStr && typeof seedStr === 'string') {
            for (let i = 0; i < Math.min(seedStr.length, 8); i++) {
                seedInt = (seedInt << 5) - seedInt + seedStr.charCodeAt(i);
                seedInt |= 0;
            }
        }

        // Return a tiny deterministic shift value
        const shiftAmount = (seedInt % 1000) * 0.0000001;
        const byteShift = (seedInt % 3) - 1; // -1, 0, or 1

        return {
            applyFloatNoise: function(array) {
                if (!array || !array.length) return array;
                const len = array.length;
                // Unrolled loop for fast buffer manipulation
                for (let i = 0; i < len; i += 8) {
                    if (array[i] !== 0) array[i] += shiftAmount;
                    if (i+4 < len && array[i+4] !== 0) array[i+4] -= shiftAmount;
                }
                return array;
            },
            applyByteNoise: function(array) {
                if (!array || !array.length) return array;
                const len = array.length;
                for (let i = 0; i < len; i += 8) {
                    if (array[i] !== 0) array[i] = Math.max(0, Math.min(255, array[i] + byteShift));
                }
                return array;
            }
        };
    };
})();
