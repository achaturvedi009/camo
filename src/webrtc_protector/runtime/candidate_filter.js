(function() {
    window.__CAMO_CANDIDATE_FILTER = function(candidateObj, proxyIp, mode) {
        if (!candidateObj || !candidateObj.candidate) return candidateObj;
        if (mode === "disable") return null;

        const candidateStr = candidateObj.candidate;
        const localIpRegex = /(192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|127\.0\.0\.1)/;

        if (localIpRegex.test(candidateStr) || candidateStr.includes('.local')) {
            return null; // Block it
        }

        return candidateObj;
    };
})();
