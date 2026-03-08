(function(fp) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) return;

    // Use profile seed to predictably generate device ID hashes
    const seed = fp.profile_id || "default_camo_seed";
    const generateId = (prefix) => {
        let hash = 0;
        const str = seed + prefix;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash |= 0;
        }
        return Math.abs(hash).toString(16).padStart(16, '0'); // Pseudo 64-bit looking hex string
    };

    const devices = [
        {
            deviceId: generateId("audioinput"),
            kind: "audioinput",
            label: "Microphone (Realtek High Definition Audio)",
            groupId: generateId("group_audio")
        },
        {
            deviceId: generateId("videoinput"),
            kind: "videoinput",
            label: "Integrated Webcam HD",
            groupId: generateId("group_video")
        },
        {
            deviceId: generateId("audiooutput"),
            kind: "audiooutput",
            label: "Speakers (Realtek Audio)",
            groupId: generateId("group_audio")
        }
    ];

    const originalEnumerate = navigator.mediaDevices.enumerateDevices;
    const spoofedEnumerate = function enumerateDevices() {
        // Return a Promise resolving to our spoofed list mapped natively
        // Mocking MediaDeviceInfo prototype to pass `instanceof MediaDeviceInfo`
        const mockDevices = devices.map(d => {
            const dev = Object.create(MediaDeviceInfo.prototype);
            Object.defineProperty(dev, 'deviceId', { value: d.deviceId, enumerable: true });
            Object.defineProperty(dev, 'kind', { value: d.kind, enumerable: true });
            Object.defineProperty(dev, 'label', { value: d.label, enumerable: true });
            Object.defineProperty(dev, 'groupId', { value: d.groupId, enumerable: true });
            return dev;
        });
        return Promise.resolve(mockDevices);
    };
    spoofedEnumerate.toString = () => "function enumerateDevices() { [native code] }";

    Object.defineProperty(navigator.mediaDevices.__proto__, 'enumerateDevices', {
        value: spoofedEnumerate,
        writable: true,
        enumerable: true,
        configurable: true
    });
})(window.__CAMO_FP__);
