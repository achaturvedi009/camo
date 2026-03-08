(function(fp) {
    if (!window.navigator || !window.navigator.permissions) return;

    const originalQuery = window.navigator.permissions.query;

    // Get permissions from injected config, or use safe defaults
    const rules = (fp && fp.permissions) ? fp.permissions : {
        'notifications': 'default',
        'geolocation': 'prompt',
        'camera': 'prompt',
        'microphone': 'prompt',
        'clipboard-read': 'prompt',
        'clipboard-write': 'granted',
        'midi': 'prompt',
        'background-sync': 'granted',
        'accelerometer': 'granted',
        'gyroscope': 'granted',
        'magnetometer': 'granted',
        'payment-handler': 'granted',
        'persistent-storage': 'prompt'
    };

    window.navigator.permissions.query = async function(parameters) {
        if (!parameters || !parameters.name) {
            throw new TypeError("Failed to execute 'query' on 'Permissions': 1 argument required, but only 0 present.");
        }

        const name = parameters.name;

        if (rules.hasOwnProperty(name)) {
            const state = rules[name];
            // If the browser natively doesn't support the permission, originalQuery might throw.
            // But we should return a resolved Promise with our mocked status.
            return Promise.resolve(window.__createPermissionStatus(state, name));
        }

        // Fallback to original
        return originalQuery.call(window.navigator.permissions, parameters);
    };

    // Mask toString
    window.navigator.permissions.query.toString = () => "function query() { [native code] }";
})(window.__CAMO_FP__);
