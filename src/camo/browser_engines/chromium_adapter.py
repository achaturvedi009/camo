class ChromiumAdapter:
    def get_launch_args(self, profile):
        return ["--disable-blink-features=AutomationControlled"]
    def apply_runtime_spoofing(self, context, script):
        # Native Playwright
        pass
