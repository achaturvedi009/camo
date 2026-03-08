(function(fp) {
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = parameters => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
        ['geolocation', 'camera', 'microphone'].includes(parameters.name) ?
            Promise.resolve({ state: 'prompt' }) :
            originalQuery.call(window.navigator.permissions, parameters)
    );
    window.navigator.permissions.query.toString = () => "function query() { [native code] }";
})(window.__CAMO_FP__);
