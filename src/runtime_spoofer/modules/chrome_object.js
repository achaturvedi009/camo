(function(fp) {
    if (fp.userAgent.includes('Chrome')) {
        if (!window.chrome) window.chrome = {};
        window.chrome.runtime = window.chrome.runtime || {};
        window.chrome.app = window.chrome.app || {};
        window.chrome.webstore = window.chrome.webstore || {};
        window.chrome.csi = function() { return { startE: Date.now(), onloadT: Date.now() + 100, pageT: 200, pt: 0, tran: 15 }; };
        window.chrome.loadTimes = function() { return { requestTime: Date.now() / 1000, startLoadTime: Date.now() / 1000, commitLoadTime: Date.now() / 1000 }; };
    }
})(window.__CAMO_FP__);
