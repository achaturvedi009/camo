import asyncio
import os
import subprocess
import json
from typing import Dict, Optional
from .profile_manager import Profile, profile_manager
from pydantic import BaseModel

class BrowserManager:
    def __init__(self):
        self.active_processes: Dict[str, subprocess.Popen] = {}

    def start_profile(self, profile_id: str) -> bool:
        profile = profile_manager.get_profile(profile_id)
        if not profile:
            raise ValueError("Profile not found")

        if profile_id in self.active_processes:
            # Check if process is still running
            proc = self.active_processes[profile_id]
            if proc.poll() is None:
                raise ValueError("Browser already running for this profile")
            else:
                del self.active_processes[profile_id]

        user_data_dir = profile_manager.get_profile_dir(profile_id)
        os.makedirs(user_data_dir, exist_ok=True)

        profile_data = {
            "id": profile.id,
            "os": profile.os,
            "user_data_dir": user_data_dir,
            "proxy": profile.proxy.model_dump() if profile.proxy else None
        }

        # Spawn child process
        cmd = ["python", "-m", "src.core.browser_worker", json.dumps(profile_data)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.active_processes[profile_id] = proc

        return True

    def stop_profile(self, profile_id: str) -> bool:
        if profile_id in self.active_processes:
            proc = self.active_processes[profile_id]
            if proc.poll() is None:
                proc.terminate()
            del self.active_processes[profile_id]
            return True
        return False

    def is_running(self, profile_id: str) -> bool:
        if profile_id in self.active_processes:
            proc = self.active_processes[profile_id]
            if proc.poll() is None:
                return True
            else:
                del self.active_processes[profile_id]
        return False

browser_manager = BrowserManager()
