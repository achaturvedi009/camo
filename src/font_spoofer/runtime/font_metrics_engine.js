(function() {
    window.__CAMO_FONT_ENGINE = function(fontsList) {
        // Simple fast lookup map for allowed fonts
        const validFonts = new Set();
        if (fontsList) {
            for (let i = 0; i < fontsList.length; i++) {
                validFonts.add(fontsList[i].toLowerCase().replace(/['"]/g, ''));
            }
        }

        return {
            isValidFont: function(fontFamilyString) {
                // If checking generic families, always valid
                const generics = ['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy'];
                if (!fontFamilyString) return true;

                const parts = fontFamilyString.split(',').map(s => s.trim().toLowerCase().replace(/['"]/g, ''));

                // If any of the requested fonts are in our "installed" list or are generic, we consider it valid for rendering
                for (let i=0; i<parts.length; i++) {
                    if (validFonts.has(parts[i]) || generics.includes(parts[i])) return true;
                }
                return false;
            },
            // Modify a dimension slightly to simulate a "fallback" font if it doesn't exist
            shiftMetrics: function(value, isAvailable) {
                if (!isAvailable && value > 0) {
                    // Shift width slightly so it looks like it fell back to a default system font
                    return value + (value * 0.05);
                }
                return value;
            }
        };
    };
})();
