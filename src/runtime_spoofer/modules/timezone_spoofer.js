(function(fp) {
    const tz = fp.timezone;
    if (tz) {
        const OriginalDateTimeFormat = Intl.DateTimeFormat;
        Intl.DateTimeFormat = function(locales, options) {
            const opts = options || {};
            if (!opts.timeZone) {
                opts.timeZone = tz;
            }
            return new OriginalDateTimeFormat(locales, opts);
        };
        Intl.DateTimeFormat.prototype = OriginalDateTimeFormat.prototype;
        Intl.DateTimeFormat.supportedLocalesOf = OriginalDateTimeFormat.supportedLocalesOf;

        const originalResolvedOptions = Intl.DateTimeFormat.prototype.resolvedOptions;
        Intl.DateTimeFormat.prototype.resolvedOptions = function() {
            const res = originalResolvedOptions.call(this);
            res.timeZone = tz;
            return res;
        };
        Intl.DateTimeFormat.prototype.resolvedOptions.toString = () => "function resolvedOptions() { [native code] }";
    }
})(window.__CAMO_FP__);
