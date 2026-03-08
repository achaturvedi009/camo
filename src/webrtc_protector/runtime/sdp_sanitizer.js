(function() {
    window.__CAMO_SDP_SANITIZER = function(sdpStr, proxyIp, mode) {
        if (!sdpStr) return sdpStr;
        if (mode === "disable") return ""; // Strips completely if disabled

        let sanitized = sdpStr;
        // Regex to match local IPs (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
        const localIpRegex = /(192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|127\.0\.0\.1)/g;

        // Remove lines containing local IPs completely, or mask them.
        // For ICE candidates inside SDP, removing the line is usually safer
        const lines = sanitized.split('\n');
        const safeLines = lines.map(line => {
            if (line.indexOf('a=candidate') === 0) {
                if (localIpRegex.test(line)) {
                    return null; // drop local candidate line
                }
                // If proxyIp exists, we could force replace public IPs with proxyIp here
                // but usually public IPs aren't gathered unless STUN is used,
                // which proxy settings naturally handle if browser proxy is correctly set.
                // We'll aggressively strip out .local mdns too just in case.
                if (line.includes('.local')) return null;
            }
            return line;
        }).filter(line => line !== null);

        return safeLines.join('\n');
    };
})();
