(function(fp) {
    if (!window.AudioBuffer || !window.OfflineAudioContext || !window.AnalyserNode) return;

    const seed = (fp.rendering && fp.rendering.audio_hash) ? fp.rendering.audio_hash : "audio_default";
    const noiseEngine = window.__CAMO_AUDIO_NOISE(seed);

    // 1. AudioBuffer.prototype.getChannelData
    const originalGetChannelData = window.AudioBuffer.prototype.getChannelData;
    const spoofedGetChannelData = function getChannelData(channel) {
        const data = originalGetChannelData.call(this, channel);
        return noiseEngine.applyFloatNoise(data);
    };
    spoofedGetChannelData.toString = () => "function getChannelData() { [native code] }";
    Object.defineProperty(window.AudioBuffer.prototype, 'getChannelData', { value: spoofedGetChannelData, writable: true, enumerable: true, configurable: true });

    // 2. AudioBuffer.prototype.copyFromChannel
    const originalCopyFromChannel = window.AudioBuffer.prototype.copyFromChannel;
    const spoofedCopyFromChannel = function copyFromChannel(destination, channelNumber, startInChannel) {
        originalCopyFromChannel.call(this, destination, channelNumber, startInChannel);
        noiseEngine.applyFloatNoise(destination);
    };
    spoofedCopyFromChannel.toString = () => "function copyFromChannel() { [native code] }";
    Object.defineProperty(window.AudioBuffer.prototype, 'copyFromChannel', { value: spoofedCopyFromChannel, writable: true, enumerable: true, configurable: true });

    // 3. AnalyserNode
    const patchAnalyserMethod = (methodName, isByte = false) => {
        const original = window.AnalyserNode.prototype[methodName];
        const spoofed = function(array) {
            original.call(this, array);
            if (isByte) {
                noiseEngine.applyByteNoise(array);
            } else {
                noiseEngine.applyFloatNoise(array);
            }
        };
        spoofed.toString = () => `function ${methodName}() { [native code] }`;
        Object.defineProperty(window.AnalyserNode.prototype, methodName, { value: spoofed, writable: true, enumerable: true, configurable: true });
    };

    patchAnalyserMethod('getFloatFrequencyData', false);
    patchAnalyserMethod('getByteFrequencyData', true);
    patchAnalyserMethod('getFloatTimeDomainData', false);
    patchAnalyserMethod('getByteTimeDomainData', true);

    // 4. OfflineAudioContext
    const originalStartRendering = window.OfflineAudioContext.prototype.startRendering;
    const spoofedStartRendering = function startRendering() {
        return originalStartRendering.call(this).then(buffer => {
            // Apply noise to all channels of the rendered buffer
            if (buffer && buffer.numberOfChannels) {
                for (let i = 0; i < buffer.numberOfChannels; i++) {
                    const channelData = originalGetChannelData.call(buffer, i);
                    noiseEngine.applyFloatNoise(channelData);
                }
            }
            return buffer;
        });
    };
    spoofedStartRendering.toString = () => "function startRendering() { [native code] }";
    Object.defineProperty(window.OfflineAudioContext.prototype, 'startRendering', { value: spoofedStartRendering, writable: true, enumerable: true, configurable: true });

    // Also properties like sampleRate could be mocked if needed, but AudioContext gets them from hardware.
    // If we want to mock baseLatency:
    if (window.AudioContext) {
        const expectedLatency = (fp.rendering && fp.rendering.audio && fp.rendering.audio.base_latency) ? fp.rendering.audio.base_latency : 0.01;
        const origBaseLatency = Object.getOwnPropertyDescriptor(window.AudioContext.prototype, 'baseLatency');
        if (origBaseLatency) {
            const spoofedLatency = function baseLatency() { return expectedLatency; };
            spoofedLatency.toString = () => "function baseLatency() { [native code] }";
            Object.defineProperty(window.AudioContext.prototype, 'baseLatency', {
                get: spoofedLatency,
                enumerable: true,
                configurable: true
            });
        }
    }

})(window.__CAMO_FP__);
