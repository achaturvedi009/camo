(function(fp) {
    const audioHash = fp.audioHash;

    // Very lightweight deterministic shift for audio context
    if (window.AudioBuffer && window.AudioBuffer.prototype.getChannelData) {
        const originalGetChannelData = window.AudioBuffer.prototype.getChannelData;
        window.AudioBuffer.prototype.getChannelData = function(channel) {
            const data = originalGetChannelData.call(this, channel);
            if (data && data.length > 0) {
                const shift = audioHash.charCodeAt(0) * 0.0000001;
                data[0] += shift;
            }
            return data;
        };
        window.AudioBuffer.prototype.getChannelData.toString = () => "function getChannelData() { [native code] }";
    }
})(window.__CAMO_FP__);
