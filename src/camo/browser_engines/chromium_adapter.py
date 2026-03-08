class ChromiumAdapter:
    def get_launch_args(self, profile):
        return [
            "--disable-blink-features=AutomationControlled",
            f"--user-data-dir={profile.get('user_data_dir')}",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--no-default-browser-check"
        ]

    def apply_runtime_spoofing(self, context, script):
        pass # add_init_script handles this usually
