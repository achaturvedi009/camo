(function(fp) {
    if (!window.RTCPeerConnection) return;

    // Get configs
    const networkInfo = fp.network || {};
    const mode = networkInfo.webrtc_protection || "proxy-only"; // "disabled", "proxy-only"
    const proxyIp = networkInfo.public_ip || "0.0.0.0";

    const sanitizeSdp = window.__CAMO_SDP_SANITIZER;
    const filterCandidate = window.__CAMO_CANDIDATE_FILTER;

    // 1. Override createOffer
    const originalCreateOffer = RTCPeerConnection.prototype.createOffer;
    const spoofedCreateOffer = function createOffer(...args) {
        if (mode === "disabled") {
            // Can reject or return empty
            return Promise.reject(new DOMException("WebRTC disabled"));
        }
        return originalCreateOffer.apply(this, args).then(offer => {
            if (offer && offer.sdp) {
                offer.sdp = sanitizeSdp(offer.sdp, proxyIp, mode);
            }
            return offer;
        });
    };
    spoofedCreateOffer.toString = () => "function createOffer() { [native code] }";
    Object.defineProperty(RTCPeerConnection.prototype, 'createOffer', { value: spoofedCreateOffer, writable: true, enumerable: true, configurable: true });

    // 2. Override createAnswer
    const originalCreateAnswer = RTCPeerConnection.prototype.createAnswer;
    const spoofedCreateAnswer = function createAnswer(...args) {
        if (mode === "disabled") return Promise.reject(new DOMException("WebRTC disabled"));
        return originalCreateAnswer.apply(this, args).then(answer => {
            if (answer && answer.sdp) {
                answer.sdp = sanitizeSdp(answer.sdp, proxyIp, mode);
            }
            return answer;
        });
    };
    spoofedCreateAnswer.toString = () => "function createAnswer() { [native code] }";
    Object.defineProperty(RTCPeerConnection.prototype, 'createAnswer', { value: spoofedCreateAnswer, writable: true, enumerable: true, configurable: true });

    // 3. Override setLocalDescription (sometimes scripts inspect what is set locally)
    const originalSetLocalDescription = RTCPeerConnection.prototype.setLocalDescription;
    const spoofedSetLocalDescription = function setLocalDescription(...args) {
        if (args.length > 0 && args[0] && args[0].sdp) {
            args[0].sdp = sanitizeSdp(args[0].sdp, proxyIp, mode);
        }
        return originalSetLocalDescription.apply(this, args);
    };
    spoofedSetLocalDescription.toString = () => "function setLocalDescription() { [native code] }";
    Object.defineProperty(RTCPeerConnection.prototype, 'setLocalDescription', { value: spoofedSetLocalDescription, writable: true, enumerable: true, configurable: true });

    // 4. Intercept onicecandidate getter/setter
    // This is tricky. Some sites use addEventListener('icecandidate'), some use peer.onicecandidate = ...
    // We override addEventListener and the property descriptor.

    const originalAddEventListener = RTCPeerConnection.prototype.addEventListener;
    const spoofedAddEventListener = function addEventListener(type, listener, options) {
        if (type === 'icecandidate' && typeof listener === 'function') {
            const wrappedListener = function(event) {
                if (event.candidate) {
                    const safeCandidate = filterCandidate(event.candidate, proxyIp, mode);
                    if (!safeCandidate) {
                        return; // Drop event
                    }
                    // We can't easily mutate event.candidate as it's readonly,
                    // but we blocked the bad ones. The safe ones pass through.
                }
                return listener.apply(this, arguments);
            };
            return originalAddEventListener.call(this, type, wrappedListener, options);
        }
        return originalAddEventListener.apply(this, arguments);
    };
    spoofedAddEventListener.toString = () => "function addEventListener() { [native code] }";
    Object.defineProperty(RTCPeerConnection.prototype, 'addEventListener', { value: spoofedAddEventListener, writable: true, enumerable: true, configurable: true });

    // Override the property descriptor for onicecandidate
    const nativeIceDesc = Object.getOwnPropertyDescriptor(RTCPeerConnection.prototype, 'onicecandidate');
    if (nativeIceDesc) {
        Object.defineProperty(RTCPeerConnection.prototype, 'onicecandidate', {
            get: function() {
                return this.__camo_ice_listener || null;
            },
            set: function(listener) {
                if (typeof listener === 'function') {
                    this.__camo_ice_listener = listener;
                    const wrappedListener = function(event) {
                        if (event.candidate) {
                            const safeCandidate = filterCandidate(event.candidate, proxyIp, mode);
                            if (!safeCandidate) return;
                        }
                        return listener.apply(this, arguments);
                    };
                    nativeIceDesc.set.call(this, wrappedListener);
                } else {
                    this.__camo_ice_listener = null;
                    nativeIceDesc.set.call(this, listener);
                }
            },
            enumerable: true,
            configurable: true
        });
    }

})(window.__CAMO_FP__);
