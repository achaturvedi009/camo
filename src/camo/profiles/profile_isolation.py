import os

class ProfileIsolationSystem:
    @staticmethod
    def get_isolation_args(profile_dir: str) -> list:
        """
        Returns arguments ensuring Playwright / Chromium completely isolates user contexts.
        """
        return [
            f"--user-data-dir={profile_dir}",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--no-default-browser-check"
        ]
