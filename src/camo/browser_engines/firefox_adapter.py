class FirefoxAdapter:
    def get_launch_args(self, profile):
        return ["--wait-for-browser"]
    def apply_runtime_spoofing(self, context, script):
        pass
