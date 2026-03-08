(function() {
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.loadTimes) {
        window.chrome.loadTimes = function loadTimes() {
            const timing = window.performance.timing || {navigationStart: Date.now()};
            const start = timing.navigationStart / 1000;
            return {
                requestTime: start + 0.01,
                startLoadTime: start,
                commitLoadTime: start + 0.02,
                finishDocumentLoadTime: start + 0.05,
                finishLoadTime: start + 0.08,
                firstPaintTime: start + 0.04,
                firstPaintAfterLoadTime: 0,
                navigationType: "Other",
                wasFetchedViaSpdy: true,
                wasNpnNegotiated: true,
                npnNegotiatedProtocol: "h2",
                wasAlternateProtocolAvailable: false,
                connectionInfo: "h2"
            };
        };
        window.chrome.loadTimes.toString = () => "function loadTimes() { [native code] }";
    }
})();
