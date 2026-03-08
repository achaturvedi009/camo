class DisplayProfileManager:
    @staticmethod
    def get_display_config(fingerprint: dict) -> dict:
        """
        Validates screen properties implicitly mapping from the core CAMO framework constraints.
        """
        if "hardware" not in fingerprint:
            return {}

        screen = fingerprint["hardware"].get("screen_resolution", "1920x1080")
        try:
            w, h = map(int, screen.split('x'))
        except:
            w, h = 1920, 1080

        dpr = fingerprint["hardware"].get("devicePixelRatio", 1.0)
        color_depth = fingerprint["hardware"].get("color_depth", 24)

        return {
            "screen_width": w,
            "screen_height": h,
            "avail_width": w,
            "avail_height": h - 40 if h > 40 else h,
            "device_pixel_ratio": dpr,
            "color_depth": color_depth
        }
