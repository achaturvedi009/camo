(function() {
    if (!window.chrome) window.chrome = {};
    if (!window.chrome.app) {
        window.chrome.app = {
            isInstalled: false,
            getIsInstalled: function() { return false; },
            getDetails: function() { return null; },
            runningState: function() { return "cannot_run"; },
            InstallState: { DISABLED: "disabled", INSTALLED: "installed", NOT_INSTALLED: "not_installed" },
            RunningState: { CANNOT_RUN: "cannot_run", READY_TO_RUN: "ready_to_run", RUNNING: "running" }
        };

        window.chrome.app.getIsInstalled.toString = () => `function getIsInstalled() { [native code] }`;
        window.chrome.app.getDetails.toString = () => `function getDetails() { [native code] }`;
        window.chrome.app.runningState.toString = () => `function runningState() { [native code] }`;
    }
})();
