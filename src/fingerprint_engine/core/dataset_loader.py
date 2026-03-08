import json
import os
from functools import lru_cache

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets")

@lru_cache(maxsize=16)
def load_dataset(filename: str):
    filepath = os.path.join(DATASET_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

class DatasetManager:
    @staticmethod
    def get_gpus(): return load_dataset("gpu.json")
    @staticmethod
    def get_cpus(): return load_dataset("cpu.json")
    @staticmethod
    def get_rams(): return load_dataset("ram.json")
    @staticmethod
    def get_screens(): return load_dataset("screens.json")
    @staticmethod
    def get_user_agents(): return load_dataset("useragents.json")
    @staticmethod
    def get_languages(): return load_dataset("languages.json")
    @staticmethod
    def get_fonts(os_type: str):
        if os_type == "windows": return load_dataset("fonts_windows.json")[0]
        elif os_type == "mac": return load_dataset("fonts_mac.json")[0]
        else: return load_dataset("fonts_linux.json")[0]
    @staticmethod
    def get_timezones(): return load_dataset("timezone_by_country.json")
    @staticmethod
    def get_webgl_profiles(): return load_dataset("webgl_profiles.json")
    @staticmethod
    def get_audio_profiles(): return load_dataset("audio_profiles.json")
