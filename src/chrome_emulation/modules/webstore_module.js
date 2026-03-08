(function() {
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.webstore) {
        window.chrome.webstore = {
            install: function install(url, onSuccess, onFailure) {},
            onInstallStageChanged: { addListener: function() {}, removeListener: function() {} },
            onDownloadProgress: { addListener: function() {}, removeListener: function() {} }
        };

        window.chrome.webstore.install.toString = () => `function install() { [native code] }`;
    }
})();
