import json
import os
from functools import lru_cache

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets")

@lru_cache(maxsize=4)
def get_fonts_for_os(os_type: str) -> list:
    os_type = os_type.lower()
    filename = f"fonts_{os_type}.json"
    if os_type == "mac":
        filename = "fonts_macos.json"

    filepath = os.path.join(DATASET_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
