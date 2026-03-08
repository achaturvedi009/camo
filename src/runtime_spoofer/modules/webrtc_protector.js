(function(fp) {
    // If WebRTC is blocked/protected (could be extended based on FP settings)
    const originalCreateOffer = RTCPeerConnection.prototype.createOffer;
    RTCPeerConnection.prototype.createOffer = function(...args) {
        return originalCreateOffer.apply(this, args).then(offer => {
            // Strip out local IPs from SDP
            offer.sdp = offer.sdp.replace(/a=candidate.*(?:192\.168|10\.|172\.(?:1[6-9]|2\d|3[0-1]))\.[\d\.]+/g, '');
            return offer;
        });
    };
    RTCPeerConnection.prototype.createOffer.toString = () => "function createOffer() { [native code] }";
})(window.__CAMO_FP__);
