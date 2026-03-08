(function(fp) {
    const override = (obj, prop, value) => {
        try {
            Object.defineProperty(obj, prop, {
                get: () => value,
                set: () => {},
                enumerable: true,
                configurable: true
            });
        } catch(e) {}
    };

    override(navigator, 'userAgent', fp.userAgent);
    override(navigator, 'platform', fp.platform);
    override(navigator, 'hardwareConcurrency', fp.cpu);
    override(navigator, 'deviceMemory', fp.ram);
    override(navigator, 'languages', fp.languages);
    override(navigator, 'language', fp.languages[0]);
    override(navigator, 'webdriver', false);

    if (fp.touchSupport) {
        override(navigator, 'maxTouchPoints', 5);
        if(!window.TouchEvent) window.TouchEvent = function() {};
    } else {
        override(navigator, 'maxTouchPoints', 0);
    }

    // Prevent detection of modification
    const getOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
    Object.getOwnPropertyDescriptor = function(obj, prop) {
        const desc = getOwnPropertyDescriptor(obj, prop);
        if (obj === navigator && ['webdriver', 'userAgent'].includes(prop)) {
            desc.get.toString = () => "function get " + prop + "() { [native code] }";
        }
        return desc;
    };
})(window.__CAMO_FP__);
