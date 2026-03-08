(function() {
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.csi) {
        window.chrome.csi = function csi() {
            const startE = performance.timing ? performance.timing.navigationStart : Date.now();
            return {
                startE: startE,
                onloadT: startE + 100,
                pageT: 150.3,
                pt: 0,
                tran: 15
            };
        };
        window.chrome.csi.toString = () => "function csi() { [native code] }";
    }
})();
