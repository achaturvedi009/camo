(function() {
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.runtime) {
        window.chrome.runtime = {
            connect: function connect() { return { onMessage: { addListener: function() {} }, postMessage: function() {}, disconnect: function() {} }; },
            sendMessage: function sendMessage(extensionId, message, options, responseCallback) {},
            getManifest: function getManifest() { return undefined; },
            id: undefined
        };

        window.chrome.runtime.connect.toString = () => `function connect() { [native code] }`;
        window.chrome.runtime.sendMessage.toString = () => `function sendMessage() { [native code] }`;
        window.chrome.runtime.getManifest.toString = () => `function getManifest() { [native code] }`;
    }
})();
