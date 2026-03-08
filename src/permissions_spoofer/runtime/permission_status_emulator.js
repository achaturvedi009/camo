(function() {
    // We only create this if it's missing or we want to override carefully.
    // Actually, rather than creating from scratch, we use a proxy or object with the correct prototype.
    // Browsers have PermissionStatus.prototype.

    window.__createPermissionStatus = function(state, name) {
        // Create an object that inherits from native PermissionStatus prototype
        let proto = null;
        try {
            proto = PermissionStatus.prototype;
        } catch(e) {
            // Fallback if PermissionStatus doesn't exist directly
            proto = EventTarget.prototype;
        }

        const statusObj = Object.create(proto);

        Object.defineProperty(statusObj, 'state', {
            value: state,
            writable: false,
            enumerable: true,
            configurable: true
        });

        Object.defineProperty(statusObj, 'name', {
            value: name,
            writable: false,
            enumerable: true,
            configurable: true
        });

        Object.defineProperty(statusObj, 'onchange', {
            value: null,
            writable: true,
            enumerable: true,
            configurable: true
        });

        // Ensure toStringTag is correct
        if (typeof Symbol !== 'undefined' && Symbol.toStringTag) {
            Object.defineProperty(statusObj, Symbol.toStringTag, {
                value: 'PermissionStatus',
                writable: false,
                enumerable: false,
                configurable: true
            });
        }

        return statusObj;
    };
})();
