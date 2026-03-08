import hashlib
import random
from typing import Any, List

class SeedEngine:
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.seed_int = int(hashlib.sha256(profile_id.encode('utf-8')).hexdigest(), 16)

    def pick(self, dataset: List[Any], offset: int = 0) -> Any:
        if not dataset:
            return None
        index = (self.seed_int + offset) % len(dataset)
        return dataset[index]

    def random_float(self, start: float, end: float, offset: int = 0) -> float:
        r = random.Random(self.seed_int + offset)
        return start + (r.random() * (end - start))

    def random_int(self, start: int, end: int, offset: int = 0) -> int:
        r = random.Random(self.seed_int + offset)
        return r.randint(start, end)

    def deterministic_hash(self, base: str, offset: int = 0) -> str:
        data = f"{self.profile_id}_{base}_{offset}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
